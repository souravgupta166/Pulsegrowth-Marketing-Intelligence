
"""Build the PulseGrowth DuckDB analytics warehouse."""

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "synthetic"
PROCESSED_DIR = ROOT / "data" / "processed"
DB_PATH = PROCESSED_DIR / "pulsegrowth.duckdb"


def csv_reader(filename: str) -> str:
    path = (DATA_DIR / filename).resolve().as_posix()
    escaped = path.replace("'", "''")
    return f"read_csv_auto('{escaped}', header = true)"


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        "campaigns.csv",
        "ad_spend.csv",
        "users.csv",
        "app_events.csv",
        "subscriptions.csv",
        "crm_experiments.csv",
        "geo_experiments.csv",
    ]

    missing = [
        name for name in required_files
        if not (DATA_DIR / name).exists()
    ]

    if missing:
        raise FileNotFoundError(
            f"Missing input files: {missing}. "
            "Run the data generator first."
        )

    con = duckdb.connect(str(DB_PATH))

    source_tables = {
        "dim_campaigns": "campaigns.csv",
        "fct_ad_spend": "ad_spend.csv",
        "fct_users": "users.csv",
        "fct_app_events": "app_events.csv",
        "fct_subscriptions": "subscriptions.csv",
        "fct_crm_experiments": "crm_experiments.csv",
        "fct_geo_experiments": "geo_experiments.csv",
    }

    print("Building PulseGrowth warehouse...")

    for table, filename in source_tables.items():
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM {csv_reader(filename)}
            """
        )

        count = con.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count:,} rows")

    # Campaign performance.
    # Aggregate each source separately before joining to prevent fan-out.
    con.execute("""
        CREATE OR REPLACE TABLE mart_campaign_performance AS
        WITH spend AS (
            SELECT
                campaign_id,
                channel,
                SUM(spend_eur) AS spend_eur,
                SUM(impressions) AS impressions,
                SUM(clicks) AS clicks
            FROM fct_ad_spend
            GROUP BY campaign_id, channel
        ),

        installs AS (
            SELECT
                campaign_id,
                COUNT(*) AS attributed_installs
            FROM fct_users
            WHERE campaign_id IS NOT NULL
            GROUP BY campaign_id
        ),

        paying_users AS (
            SELECT
                u.campaign_id,
                COUNT(DISTINCT u.user_id) AS paying_customers
            FROM fct_users u
            INNER JOIN (
                SELECT DISTINCT user_id
                FROM fct_subscriptions
            ) s USING (user_id)
            WHERE u.campaign_id IS NOT NULL
            GROUP BY u.campaign_id
        ),

        revenue AS (
            SELECT
                u.campaign_id,
                SUM(s.revenue_eur) AS attributed_revenue_eur
            FROM fct_users u
            INNER JOIN fct_subscriptions s USING (user_id)
            WHERE u.campaign_id IS NOT NULL
            GROUP BY u.campaign_id
        )

        SELECT
            c.campaign_id,
            c.campaign_name,
            c.channel,
            c.campaign_theme,

            COALESCE(sp.spend_eur, 0) AS spend_eur,
            COALESCE(sp.impressions, 0) AS impressions,
            COALESCE(sp.clicks, 0) AS clicks,
            COALESCE(i.attributed_installs, 0) AS attributed_installs,
            COALESCE(p.paying_customers, 0) AS paying_customers,
            COALESCE(r.attributed_revenue_eur, 0)
                AS attributed_revenue_eur,

            COALESCE(sp.clicks, 0)
                / NULLIF(sp.impressions, 0)
                AS click_through_rate,

            COALESCE(sp.spend_eur, 0)
                / NULLIF(sp.clicks, 0)
                AS cost_per_click_eur,

            COALESCE(sp.spend_eur, 0)
                / NULLIF(i.attributed_installs, 0)
                AS cost_per_attributed_install_eur,

            COALESCE(sp.spend_eur, 0)
                / NULLIF(p.paying_customers, 0)
                AS customer_acquisition_cost_eur,

            COALESCE(r.attributed_revenue_eur, 0)
                / NULLIF(sp.spend_eur, 0)
                AS attributed_roas,

            COALESCE(p.paying_customers, 0)
                / NULLIF(i.attributed_installs, 0)
                AS install_to_payer_rate

        FROM dim_campaigns c
        LEFT JOIN spend sp USING (campaign_id)
        LEFT JOIN installs i USING (campaign_id)
        LEFT JOIN paying_users p USING (campaign_id)
        LEFT JOIN revenue r USING (campaign_id)
    """)

    # Retention is calculated from exact elapsed days since installation.
    # A user is eligible for D7 only if their installation was at least
    # seven days before the dataset's observation end date.
    con.execute("""
        CREATE OR REPLACE TABLE mart_cohort_retention AS
        WITH user_cohorts AS (
            SELECT
                user_id,
                CAST(install_date AS DATE) AS install_date,
                DATE_TRUNC(
                    'month',
                    CAST(install_date AS DATE)
                )::DATE AS cohort_month,
                channel,
                campaign_id
            FROM fct_users
        ),

        observed_events AS (
            SELECT DISTINCT
                user_id,
                CAST(event_date AS DATE) AS event_date
            FROM fct_app_events
            WHERE event_name = 'session_start'
        ),

        user_activity AS (
            SELECT
                u.user_id,
                u.cohort_month,
                u.channel,
                u.install_date,

                MAX(
                    CASE
                        WHEN e.event_date = u.install_date
                            + INTERVAL 1 DAY
                        THEN 1 ELSE 0
                    END
                ) AS retained_d1,

                MAX(
                    CASE
                        WHEN e.event_date = u.install_date
                            + INTERVAL 7 DAY
                        THEN 1 ELSE 0
                    END
                ) AS retained_d7,

                MAX(
                    CASE
                        WHEN e.event_date = u.install_date
                            + INTERVAL 30 DAY
                        THEN 1 ELSE 0
                    END
                ) AS retained_d30

            FROM user_cohorts u
            LEFT JOIN observed_events e USING (user_id)
            GROUP BY
                u.user_id,
                u.cohort_month,
                u.channel,
                u.install_date
        )

        SELECT
            cohort_month,
            channel,
            COUNT(*) AS cohort_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 1 DAY
                THEN 1 ELSE 0 END
            ) AS d1_eligible_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 1 DAY
                THEN retained_d1 ELSE 0 END
            ) AS d1_retained_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 7 DAY
                THEN 1 ELSE 0 END
            ) AS d7_eligible_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 7 DAY
                THEN retained_d7 ELSE 0 END
            ) AS d7_retained_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 30 DAY
                THEN 1 ELSE 0 END
            ) AS d30_eligible_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 30 DAY
                THEN retained_d30 ELSE 0 END
            ) AS d30_retained_users,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 1 DAY
                THEN retained_d1 ELSE 0 END
            )::DOUBLE / NULLIF(
                SUM(
                    CASE WHEN install_date
                        <= DATE '2026-09-30' - INTERVAL 1 DAY
                    THEN 1 ELSE 0 END
                ), 0
            ) AS d1_retention_rate,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 7 DAY
                THEN retained_d7 ELSE 0 END
            )::DOUBLE / NULLIF(
                SUM(
                    CASE WHEN install_date
                        <= DATE '2026-09-30' - INTERVAL 7 DAY
                    THEN 1 ELSE 0 END
                ), 0
            ) AS d7_retention_rate,

            SUM(
                CASE WHEN install_date
                    <= DATE '2026-09-30' - INTERVAL 30 DAY
                THEN retained_d30 ELSE 0 END
            )::DOUBLE / NULLIF(
                SUM(
                    CASE WHEN install_date
                        <= DATE '2026-09-30' - INTERVAL 30 DAY
                    THEN 1 ELSE 0 END
                ), 0
            ) AS d30_retention_rate

        FROM user_activity
        GROUP BY cohort_month, channel
    """)

    # Daily spend and attributed installs for trend analysis.
    con.execute("""
        CREATE OR REPLACE TABLE mart_daily_campaign_performance AS
        WITH installs AS (
            SELECT
                CAST(install_date AS DATE) AS date,
                campaign_id,
                COUNT(*) AS attributed_installs
            FROM fct_users
            WHERE campaign_id IS NOT NULL
            GROUP BY CAST(install_date AS DATE), campaign_id
        ),

        spend AS (
            SELECT
                CAST(date AS DATE) AS date,
                campaign_id,
                SUM(spend_eur) AS spend_eur,
                SUM(clicks) AS clicks,
                SUM(impressions) AS impressions
            FROM fct_ad_spend
            GROUP BY CAST(date AS DATE), campaign_id
        )

        SELECT
            s.date,
            s.campaign_id,
            c.channel,
            s.spend_eur,
            s.clicks,
            s.impressions,
            COALESCE(i.attributed_installs, 0)
                AS attributed_installs,

            COALESCE(i.attributed_installs, 0)::DOUBLE
                / NULLIF(s.clicks, 0)
                AS click_to_install_rate

        FROM spend s
        JOIN dim_campaigns c USING (campaign_id)
        LEFT JOIN installs i
            ON s.date = i.date
            AND s.campaign_id = i.campaign_id
    """)

    print("\nWarehouse marts created.")

    print("\nCampaign performance preview:")
    print(
        con.execute("""
            SELECT
                campaign_name,
                spend_eur,
                attributed_installs,
                paying_customers,
                customer_acquisition_cost_eur,
                attributed_roas
            FROM mart_campaign_performance
            ORDER BY attributed_roas DESC
            LIMIT 10
        """).df().to_string(index=False)
    )

    print("\nRetention preview:")
    print(
        con.execute("""
            SELECT
                cohort_month,
                channel,
                cohort_users,
                d1_retention_rate,
                d7_retention_rate,
                d30_retention_rate
            FROM mart_cohort_retention
            ORDER BY cohort_month, channel
            LIMIT 12
        """).df().to_string(index=False)
    )

    con.close()
    print(f"\nDatabase saved to: {DB_PATH}")


if __name__ == "__main__":
    main()
