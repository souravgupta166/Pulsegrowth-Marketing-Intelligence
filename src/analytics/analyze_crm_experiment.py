
"""Statistical analysis of the simulated CRM experiment."""

from pathlib import Path
import math

import duckdb
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "pulsegrowth.duckdb"
ALPHA = 0.05


def analyse(control_n, control_x, treatment_n, treatment_x):
    """Calculate conversion rates, lift, confidence interval and p-value."""
    if control_n <= 0 or treatment_n <= 0:
        raise ValueError("Both groups must have at least one user.")

    if not (0 <= control_x <= control_n and 0 <= treatment_x <= treatment_n):
        raise ValueError("Conversions must be between zero and assigned users.")

    p_control = control_x / control_n
    p_treatment = treatment_x / treatment_n

    absolute_lift = p_treatment - p_control
    relative_lift = (
        absolute_lift / p_control if p_control > 0 else None
    )

    # Unpooled standard error for the confidence interval.
    se_ci = math.sqrt(
        p_control * (1 - p_control) / control_n
        + p_treatment * (1 - p_treatment) / treatment_n
    )

    z_critical = norm.ppf(1 - ALPHA / 2)
    ci_lower = absolute_lift - z_critical * se_ci
    ci_upper = absolute_lift + z_critical * se_ci

    # Pooled standard error for the two-proportion hypothesis test.
    pooled_rate = (
        control_x + treatment_x
    ) / (control_n + treatment_n)

    se_test = math.sqrt(
        pooled_rate * (1 - pooled_rate)
        * (1 / control_n + 1 / treatment_n)
    )

    if se_test == 0:
        p_value = 1.0 if absolute_lift == 0 else 0.0
    else:
        z_score = absolute_lift / se_test
        p_value = 2 * norm.sf(abs(z_score))

    return {
        "control_rate": p_control,
        "treatment_rate": p_treatment,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": p_value,
        "statistically_significant": bool(p_value < ALPHA),
    }


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Warehouse not found: {DB_PATH}. Build it first."
        )

    con = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        query = """
            SELECT
                experiment_id,
                segment,
                variant,
                SUM(assigned_users) AS assigned_users,
                SUM(conversions) AS conversions
            FROM analytics.mart_crm_experiment_results
            GROUP BY experiment_id, segment, variant
            ORDER BY experiment_id, segment, variant
        """
        rows = con.execute(query).fetchall()
    finally:
        con.close()

    groups = {}

    for experiment_id, segment, variant, n, x in rows:
        key = (experiment_id, segment)
        groups.setdefault(key, {})[variant] = (int(n), int(x))

    print("\nPULSEGROWTH CRM EXPERIMENT ANALYSIS")
    print("=" * 75)
    print("Dataset: synthetic; results are illustrative, not real campaign evidence.")
    print(f"Two-sided significance threshold: {ALPHA:.0%}\n")

    for (experiment_id, segment), variants in sorted(groups.items()):
        if not {"control", "treatment"}.issubset(variants):
            print(f"Skipping {segment}: a comparison group is missing.")
            continue

        control_n, control_x = variants["control"]
        treatment_n, treatment_x = variants["treatment"]

        result = analyse(
            control_n, control_x, treatment_n, treatment_x
        )

        print(f"Experiment: {experiment_id} | Segment: {segment}")
        print(
            f"  Control:   {control_x:,}/{control_n:,} "
            f"({result['control_rate']:.2%})"
        )
        print(
            f"  Treatment: {treatment_x:,}/{treatment_n:,} "
            f"({result['treatment_rate']:.2%})"
        )
        print(f"  Absolute lift: {result['absolute_lift']:+.2%}")

        if result["relative_lift"] is not None:
            print(f"  Relative lift: {result['relative_lift']:+.2%}")

        print(
            "  95% CI for lift: "
            f"[{result['ci_lower']:+.2%}, {result['ci_upper']:+.2%}]"
        )
        print(f"  Two-sided p-value: {result['p_value']:.6f}")
        print(
            "  Result at 5%: "
            + (
                "statistically significant"
                if result["statistically_significant"]
                else "not statistically significant"
            )
        )
        print()

    print("=" * 75)
    print(
        "Interpretation requires checking randomisation, sample size, "
        "outcome definitions and multiple comparisons."
    )


if __name__ == "__main__":
    main()
