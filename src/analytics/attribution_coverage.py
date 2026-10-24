
"""Audit campaign attribution coverage in PulseGrowth."""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "pulsegrowth.duckdb"


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Warehouse not found: {DB_PATH}. Build it first."
        )

    con = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        coverage_query = """
            SELECT
                channel,
                COUNT(*) AS total_installs,
                COUNT(*) FILTER (
                    WHERE campaign_id IS NOT NULL
                ) AS attributed_installs,
                COUNT(*) FILTER (
                    WHERE campaign_id IS NULL
                ) AS unattributed_installs,
                (
                    COUNT(*) FILTER (
                        WHERE campaign_id IS NOT NULL
                    )
                )::DOUBLE / NULLIF(COUNT(*), 0)
                    AS attribution_coverage
            FROM main.fct_users
            GROUP BY channel
            ORDER BY total_installs DESC
        """

        spend_query = """
            SELECT
                channel,
                ROUND(SUM(spend_eur), 2) AS total_spend_eur,
                SUM(clicks) AS total_clicks,
                SUM(impressions) AS total_impressions,
                COUNT(DISTINCT campaign_id) AS campaign_count
            FROM main.fct_ad_spend
            GROUP BY channel
            ORDER BY total_spend_eur DESC
        """

        coverage = con.execute(coverage_query).df()
        spend = con.execute(spend_query).df()

    finally:
        con.close()

    # Convert the coverage ratio into a readable percentage for display.
    coverage["attribution_coverage_pct"] = (
        coverage["attribution_coverage"] * 100
    ).round(2)
    coverage = coverage.drop(columns=["attribution_coverage"])

    print("\nATTRIBUTION COVERAGE AUDIT")
    print("=" * 90)
    print(coverage.to_string(index=False))

    print("\nCHANNEL SPEND SUMMARY")
    print("=" * 90)
    print(spend.to_string(index=False))

    print("\nINTERPRETATION")
    print("- Unattributed installs have no campaign identifier in the dataset.")
    print(
        "- Attribution coverage measures data completeness; it does not prove "
        "that advertising caused an install."
    )
    print(
        "- This audit uses synthetic attributed user data and synthetic spend."
    )
    print(
        "- True platform-to-mobile-measurement-partner reconciliation would "
        "require separate platform and attribution-provider records."
    )


if __name__ == "__main__":
    main()
