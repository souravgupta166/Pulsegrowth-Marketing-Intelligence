
"""Data quality checks for PulseGrowth synthetic CSV files."""

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "synthetic"

FILES = {
    "campaigns": "campaigns.csv",
    "ad_spend": "ad_spend.csv",
    "users": "users.csv",
    "app_events": "app_events.csv",
    "subscriptions": "subscriptions.csv",
    "crm_experiments": "crm_experiments.csv",
    "geo_experiments": "geo_experiments.csv",
}


def csv_reader(filename: str) -> str:
    path = (DATA_DIR / filename).resolve().as_posix()
    escaped = path.replace("'", "''")
    return f"read_csv_auto('{escaped}', header = true)"


def main() -> None:
    missing_files = [
        filename
        for filename in FILES.values()
        if not (DATA_DIR / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing datasets: {', '.join(missing_files)}. "
            "Run the data generator first."
        )

    con = duckdb.connect(":memory:")

    for table, filename in FILES.items():
        con.execute(
            f"CREATE VIEW {table} AS SELECT * FROM "
            f"{csv_reader(filename)}"
        )

    results = []

    def check(name: str, passed: bool, detail: str) -> None:
        results.append((name, passed, detail))

    def scalar(query: str):
        return con.execute(query).fetchone()[0]

    # Required datasets must contain rows.
    for table in FILES:
        n = scalar(f"SELECT COUNT(*) FROM {table}")
        check(
            f"{table} is non-empty",
            n > 0,
            f"{n:,} rows",
        )

    # Entity identifiers must be unique.
    for table, key in [
        ("campaigns", "campaign_id"),
        ("users", "user_id"),
        ("app_events", "event_id"),
        ("subscriptions", "transaction_id"),
    ]:
        n = scalar(
            f"""
            SELECT COUNT(*) FROM (
                SELECT {key}
                FROM {table}
                GROUP BY {key}
                HAVING COUNT(*) > 1
            )
            """
        )
        check(
            f"{table}.{key} unique",
            n == 0,
            f"{n:,} duplicate keys",
        )

    # Child records must refer to existing users.
    for table in [
        "app_events",
        "subscriptions",
        "crm_experiments",
    ]:
        n = scalar(
            f"""
            SELECT COUNT(*)
            FROM {table} child
            LEFT JOIN users parent USING (user_id)
            WHERE parent.user_id IS NULL
            """
        )
        check(
            f"{table} user references valid",
            n == 0,
            f"{n:,} orphan rows",
        )

    # Spend must reference known campaigns.
    n = scalar(
        """
        SELECT COUNT(*)
        FROM ad_spend s
        LEFT JOIN campaigns c USING (campaign_id)
        WHERE c.campaign_id IS NULL
        """
    )
    check("Ad spend campaign references valid", n == 0, f"{n:,} invalid")

    # Every attributed user must have a campaign.
    n = scalar(
        """
        SELECT COUNT(*)
        FROM users
        WHERE
            (campaign_id IS NULL AND channel <> 'Unattributed')
            OR
            (campaign_id IS NOT NULL AND channel = 'Unattributed')
        """
    )
    check("Attribution fields consistent", n == 0, f"{n:,} invalid")

    # Financial values and event chronology.
    n = scalar(
        "SELECT COUNT(*) FROM ad_spend "
        "WHERE spend_eur IS NULL OR spend_eur < 0"
    )
    check("Spend is non-negative", n == 0, f"{n:,} invalid")

    n = scalar(
        "SELECT COUNT(*) FROM subscriptions "
        "WHERE revenue_eur IS NULL OR revenue_eur <= 0"
    )
    check("Subscription revenue is positive", n == 0, f"{n:,} invalid")

    n = scalar(
        """
        SELECT COUNT(*)
        FROM app_events e
        JOIN users u USING (user_id)
        WHERE CAST(e.event_date AS DATE) < CAST(u.install_date AS DATE)
        """
    )
    check("Events do not precede installation", n == 0, f"{n:,} invalid")

    n = scalar(
        """
        SELECT COUNT(*)
        FROM subscriptions s
        JOIN users u USING (user_id)
        WHERE CAST(s.transaction_date AS DATE) < CAST(u.install_date AS DATE)
        """
    )
    check("Transactions do not precede installation", n == 0, f"{n:,} invalid")

    # CRM outcomes must be binary, and each user may be assigned once.
    n = scalar(
        """
        SELECT COUNT(*)
        FROM crm_experiments
        WHERE converted_within_7d NOT IN (0, 1)
           OR converted_within_7d IS NULL
           OR variant NOT IN ('control', 'treatment')
        """
    )
    check("CRM outcomes and variants valid", n == 0, f"{n:,} invalid")

    n = scalar(
        """
        SELECT COUNT(*) FROM (
            SELECT experiment_id, user_id
            FROM crm_experiments
            GROUP BY experiment_id, user_id
            HAVING COUNT(*) > 1
        )
        """
    )
    check("CRM assignments unique per experiment", n == 0, f"{n:,} duplicates")

    # Geo experiment flags must be binary.
    n = scalar(
        """
        SELECT COUNT(*)
        FROM geo_experiments
        WHERE treatment_group NOT IN (0, 1)
           OR experiment_period NOT IN (0, 1)
        """
    )
    check("Geo experiment flags valid", n == 0, f"{n:,} invalid")

    # Date boundaries must be valid.
    for table, column in [
        ("users", "install_date"),
        ("app_events", "event_date"),
        ("subscriptions", "transaction_date"),
        ("ad_spend", "date"),
    ]:
        n = scalar(
            f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE TRY_CAST({column} AS DATE) IS NULL
            """
        )
        check(f"{table}.{column} valid dates", n == 0, f"{n:,} invalid")

    print("\nPULSEGROWTH DATA QUALITY REPORT")
    print("=" * 75)

    for name, passed, detail in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    failures = sum(not passed for _, passed, _ in results)

    print("=" * 75)
    print(f"Passed: {len(results) - failures}/{len(results)}")

    con.close()

    if failures:
        raise SystemExit(f"{failures} validation check(s) failed.")

    print("All implemented data quality checks passed.")


if __name__ == "__main__":
    main()
