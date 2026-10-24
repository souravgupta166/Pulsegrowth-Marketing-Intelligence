
"""Build a campaign-level marketing decision table from the DuckDB warehouse."""

from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "pulsegrowth.duckdb"
OUTPUT_PATH = ROOT / "data" / "processed" / "campaign_decision_table.csv"

# Illustrative screening thresholds, not universal industry benchmarks.
MIN_CTR_FOR_REVIEW = 0.01
PROMISING_ROAS_THRESHOLD = 1.0
LOW_ROAS_THRESHOLD = 0.5


def first_available_column(df, candidates, required=True):
    """Find a column using supported alternative names."""
    for name in candidates:
        if name in df.columns:
            return name

    if required:
        raise ValueError(
            f"Could not find any of these columns: {candidates}. "
            f"Available columns: {list(df.columns)}"
        )

    return None


def safe_divide(numerator, denominator):
    """Divide safely, returning NaN when the denominator is zero or missing."""
    numerator = pd.to_numeric(numerator, errors="coerce")
    denominator = pd.to_numeric(denominator, errors="coerce")

    result = numerator.div(denominator)
    return result.where(denominator.notna() & denominator.ne(0))


def build_decision_table(source_df):
    """Calculate KPIs and transparent screening labels."""
    df = source_df.copy()

    column_map = {
        "campaign_id": first_available_column(
            df, ["campaign_id", "id"]
        ),
        "campaign_name": first_available_column(
            df, ["campaign_name", "name"]
        ),
        "channel": first_available_column(
            df, ["channel", "marketing_channel"]
        ),
        "spend": first_available_column(
            df, ["spend_eur", "spend", "total_spend_eur"]
        ),
        "impressions": first_available_column(
            df, ["impressions", "total_impressions"]
        ),
        "clicks": first_available_column(
            df, ["clicks", "total_clicks"]
        ),
        "installs": first_available_column(
            df, ["attributed_installs", "installs"]
        ),
        "paying_customers": first_available_column(
            df, ["paying_customers", "attributed_paying_customers"]
        ),
        "revenue": first_available_column(
            df, ["attributed_revenue_eur", "attributed_revenue", "revenue_eur"]
        ),
    }

    rename_map = {
        source: target
        for target, source in column_map.items()
        if source != target
    }
    df = df.rename(columns=rename_map)

    numeric_columns = [
        "spend",
        "impressions",
        "clicks",
        "installs",
        "paying_customers",
        "revenue",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df["campaign_id"].duplicated().any():
        raise ValueError(
            "Campaign IDs are not unique in the source mart. "
            "Check the dbt model before calculating campaign KPIs."
        )

    if (df[numeric_columns] < 0).any().any():
        raise ValueError("Negative values found in campaign metrics.")

    # CTR = clicks / impressions.
    df["ctr"] = safe_divide(df["clicks"], df["impressions"])

    # CPI = spend / attributed installs.
    df["cpi_eur"] = safe_divide(df["spend"], df["installs"])

    # CAC = spend / attributed paying customers.
    df["cac_eur"] = safe_divide(
        df["spend"], df["paying_customers"]
    )

    # Install-to-paying-customer conversion rate.
    df["install_to_payer_rate"] = safe_divide(
        df["paying_customers"], df["installs"]
    )

    # Initial attributed revenue per install.
    df["revenue_per_install_eur"] = safe_divide(
        df["revenue"], df["installs"]
    )

    # Attributed ROAS = attributed initial revenue / ad spend.
    df["roas"] = safe_divide(df["revenue"], df["spend"])

    # Transparent rules for screening campaigns for further investigation.
    def recommendation(row):
        if pd.isna(row["spend"]) or row["spend"] <= 0:
            return "Investigate spend data"

        if pd.isna(row["installs"]) or row["installs"] <= 0:
            return "Investigate install tracking"

        if pd.isna(row["roas"]):
            return "Investigate revenue data"

        if row["roas"] >= PROMISING_ROAS_THRESHOLD:
            return "Promising — validate before scaling"

        if row["roas"] < LOW_ROAS_THRESHOLD:
            return "Review efficiency"

        if pd.notna(row["ctr"]) and row["ctr"] < MIN_CTR_FOR_REVIEW:
            return "Review click-through rate"

        return "Monitor and optimise"

    df["recommendation"] = df.apply(recommendation, axis=1)

    # Sort by attributed ROAS, then by lower CAC.
    # Missing values appear last and are not treated as zero.
    df = df.sort_values(
        by=["roas", "cac_eur"],
        ascending=[False, True],
        na_position="last",
    ).reset_index(drop=True)

    df.insert(0, "performance_rank", range(1, len(df) + 1))

    # Keep rates as proportions in the CSV; format them as percentages
    # when displaying them in the dashboard.
    output_columns = [
        "performance_rank",
        "campaign_id",
        "campaign_name",
        "channel",
        "spend",
        "impressions",
        "clicks",
        "ctr",
        "installs",
        "cpi_eur",
        "paying_customers",
        "cac_eur",
        "install_to_payer_rate",
        "revenue",
        "revenue_per_install_eur",
        "roas",
        "recommendation",
    ]

    return df[output_columns].rename(
        columns={
            "spend": "spend_eur",
            "installs": "attributed_installs",
            "revenue": "attributed_revenue_eur",
            "ctr": "click_through_rate",
            "install_to_payer_rate": "install_to_payer_conversion_rate",
            "roas": "attributed_roas",
        }
    )


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB warehouse not found: {DB_PATH}\n"
            "Run the warehouse builder and dbt models first."
        )

    con = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        # Use the dbt-built campaign mart.
        source_df = con.execute(
            "SELECT * FROM analytics.mart_campaign_performance"
        ).df()
    finally:
        con.close()

    if source_df.empty:
        raise ValueError("Campaign performance mart contains no rows.")

    decision_table = build_decision_table(source_df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    decision_table.to_csv(OUTPUT_PATH, index=False)

    print("\nPULSEGROWTH CAMPAIGN PERFORMANCE DECISION TABLE")
    print("=" * 110)
    print(f"Campaigns analysed: {len(decision_table):,}")
    print(f"Output saved to: {OUTPUT_PATH}")
    print("\nTop campaigns by attributed ROAS:")
    print("-" * 110)

    display_columns = [
        "performance_rank",
        "campaign_name",
        "channel",
        "spend_eur",
        "attributed_installs",
        "cpi_eur",
        "cac_eur",
        "click_through_rate",
        "attributed_roas",
        "recommendation",
    ]

    display_df = decision_table[display_columns].copy()

    for col in [
        "click_through_rate",
    ]:
        display_df[col] = display_df[col].map(
            lambda value: f"{value:.2%}" if pd.notna(value) else "N/A"
        )

    for col in ["spend_eur", "cpi_eur", "cac_eur"]:
        display_df[col] = display_df[col].map(
            lambda value: f"€{value:,.2f}" if pd.notna(value) else "N/A"
        )

    display_df["attributed_roas"] = display_df["attributed_roas"].map(
        lambda value: f"{value:.2f}x" if pd.notna(value) else "N/A"
    )

    print(display_df.to_string(index=False))

    print("\nIMPORTANT INTERPRETATION NOTES")
    print("- ROAS uses attributed initial subscription revenue, not lifetime revenue.")
    print("- ROAS above 1.0x does not necessarily mean the campaign is profitable.")
    print("- Rankings describe attributed performance, not causal incrementality.")
    print("- Screening thresholds are illustrative and should be calibrated.")
    print("- Campaigns with missing or zero denominators are not assigned fake zero KPIs.")


if __name__ == "__main__":
    main()
