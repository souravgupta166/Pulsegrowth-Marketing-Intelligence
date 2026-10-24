
"""Generate synthetic mobile marketing data for PulseGrowth.

All data is fictional. No real users, health data, or platform exports
are used. The random seed makes the dataset reproducible.
"""

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
END_DATE = pd.Timestamp("2026-09-30")
START_DATE = END_DATE - pd.Timedelta(days=179)

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "data" / "synthetic"

CHANNELS = {
    "Meta Ads": {
        "daily_spend": 850,
        "cpc": 1.20,
        "install_rate": 0.32,
        "payer_rate": 0.075,
    },
    "Google Ads": {
        "daily_spend": 1000,
        "cpc": 1.45,
        "install_rate": 0.38,
        "payer_rate": 0.105,
    },
    "TikTok Ads": {
        "daily_spend": 600,
        "cpc": 0.85,
        "install_rate": 0.27,
        "payer_rate": 0.055,
    },
    "Apple Search Ads": {
        "daily_spend": 500,
        "cpc": 1.05,
        "install_rate": 0.43,
        "payer_rate": 0.12,
    },
}

CAMPAIGN_THEMES = [
    "wellness",
    "habit_builder",
    "sleep",
    "mindfulness",
]


def make_id(prefix: str, number: int) -> str:
    return f"{prefix}_{number:07d}"


def generate_campaigns(
    rng: np.random.Generator,
) -> pd.DataFrame:
    rows = []
    number = 0

    for channel, settings in CHANNELS.items():
        for theme in CAMPAIGN_THEMES:
            number += 1
            rows.append(
                {
                    "campaign_id": make_id("cmp", number),
                    "campaign_name": f"{channel}_{theme}",
                    "channel": channel,
                    "campaign_theme": theme,
                    "daily_budget_eur": round(
                        settings["daily_spend"]
                        * rng.uniform(0.65, 1.35),
                        2,
                    ),
                    "target_country": "DE",
                }
            )

    return pd.DataFrame(rows)


def generate_spend(
    campaigns: pd.DataFrame,
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
) -> pd.DataFrame:
    rows = []

    for campaign in campaigns.itertuples(index=False):
        settings = CHANNELS[campaign.channel]

        for date in dates:
            weekday_factor = (
                1.10 if date.day_of_week in (4, 5) else 0.94
            )

            spend = (
                campaign.daily_budget_eur
                * weekday_factor
                * rng.uniform(0.78, 1.20)
            )

            clicks = int(
                spend / settings["cpc"]
                * rng.uniform(0.85, 1.15)
            )

            # Impressions are generated so clicks do not exceed impressions.
            impressions = int(
                clicks / rng.uniform(0.025, 0.085)
            )

            rows.append(
                {
                    "date": date.date().isoformat(),
                    "campaign_id": campaign.campaign_id,
                    "channel": campaign.channel,
                    "spend_eur": round(spend, 2),
                    "impressions": max(impressions, clicks),
                    "clicks": clicks,
                }
            )

    return pd.DataFrame(rows)


def generate_users_and_events(
    spend: pd.DataFrame,
    campaigns: pd.DataFrame,
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate installs, user activity, and initial subscription purchases."""

    campaign_lookup = campaigns.set_index("campaign_id").to_dict("index")

    user_rows = []
    event_rows = []
    subscription_rows = []

    user_number = 0
    event_number = 0
    transaction_number = 0

    for daily in spend.itertuples(index=False):
        settings = CHANNELS[daily.channel]
        campaign = campaign_lookup[daily.campaign_id]
        install_date = pd.Timestamp(daily.date)

        install_count = rng.binomial(
            n=max(0, daily.clicks),
            p=settings["install_rate"],
        )

        for _ in range(install_count):
            user_number += 1
            user_id = make_id("usr", user_number)

            attributed = rng.random() >= 0.08
            channel = daily.channel if attributed else "Unattributed"
            campaign_id = daily.campaign_id if attributed else None

            user_rows.append(
                {
                    "user_id": user_id,
                    "install_date": install_date.date().isoformat(),
                    "campaign_id": campaign_id,
                    "channel": channel,
                    "country": "DE",
                    "platform": str(
                        rng.choice(["iOS", "Android"])
                    ),
                }
            )

            # Every generated user has an initial app-open event.
            event_number += 1
            event_rows.append(
                {
                    "event_id": make_id("evt", event_number),
                    "user_id": user_id,
                    "event_date": install_date.date().isoformat(),
                    "event_name": "app_open",
                }
            )

            # Return activity decays with time since installation.
            # This is a simulation assumption, not a measured benchmark.
            user_age_days = (END_DATE - install_date).days
            max_return_day = min(user_age_days, 30)

            for return_day in range(1, max_return_day + 1):
                return_probability = (
                    0.32 * np.exp(-0.095 * (return_day - 1))
                )

                if rng.random() < return_probability:
                    event_number += 1
                    event_date = install_date + pd.Timedelta(
                        days=return_day
                    )

                    event_rows.append(
                        {
                            "event_id": make_id("evt", event_number),
                            "user_id": user_id,
                            "event_date": event_date.date().isoformat(),
                            "event_name": "session_start",
                        }
                    )

            # Simulate whether the user becomes a paying customer.
            if rng.random() < settings["payer_rate"]:
                conversion_delay = int(rng.integers(0, 8))
                conversion_date = install_date + pd.Timedelta(
                    days=conversion_delay
                )

                if conversion_date <= END_DATE:
                    transaction_number += 1
                    amount = float(
                        rng.choice(
                            [9.99, 14.99, 19.99],
                            p=[0.45, 0.40, 0.15],
                        )
                    )

                    subscription_rows.append(
                        {
                            "transaction_id": make_id(
                                "txn", transaction_number
                            ),
                            "user_id": user_id,
                            "transaction_date": (
                                conversion_date.date().isoformat()
                            ),
                            "revenue_eur": round(amount, 2),
                            "transaction_type": "initial_subscription",
                        }
                    )

    users = pd.DataFrame(
        user_rows,
        columns=[
            "user_id",
            "install_date",
            "campaign_id",
            "channel",
            "country",
            "platform",
        ],
    )

    events = pd.DataFrame(
        event_rows,
        columns=[
            "event_id",
            "user_id",
            "event_date",
            "event_name",
        ],
    )

    subscriptions = pd.DataFrame(
        subscription_rows,
        columns=[
            "transaction_id",
            "user_id",
            "transaction_date",
            "revenue_eur",
            "transaction_type",
        ],
    )

    return users, events, subscriptions


def generate_crm_experiments(
    users: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Randomise eligible users and simulate a seven-day outcome.

    Important: this generator uses an illustrative treatment effect.
    It must not be interpreted as a real experimental finding.
    """

    columns = [
        "experiment_id",
        "user_id",
        "segment",
        "variant",
        "assigned_date",
        "converted_within_7d",
    ]

    if users.empty:
        return pd.DataFrame(columns=columns)

    eligible = users.sample(
        frac=0.60,
        random_state=SEED,
    ).reset_index(drop=True)

    rows = []
    segments = ["new_user", "inactive_user", "trial_user"]

    for user in eligible.itertuples(index=False):
        segment = str(rng.choice(segments))

        # Random assignment, independent of the generated segment.
        variant = str(rng.choice(["control", "treatment"]))

        baseline_probability = {
            "new_user": 0.08,
            "inactive_user": 0.035,
            "trial_user": 0.16,
        }[segment]

        simulated_lift = 0.025 if variant == "treatment" else 0.0
        conversion_probability = min(
            1.0,
            baseline_probability + simulated_lift,
        )

        rows.append(
            {
                "experiment_id": "crm_onboarding_v1",
                "user_id": user.user_id,
                "segment": segment,
                "variant": variant,
                "assigned_date": user.install_date,
                "converted_within_7d": int(
                    rng.random() < conversion_probability
                ),
            }
        )

    return pd.DataFrame(rows, columns=columns)


def generate_geo_experiment(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate illustrative market-level outcomes for geo-lift analysis.

    Two markets receive treatment. Since there are only four markets and
    assignment is not randomised, results are for methodology practice only.
    """

    markets = ["DE_NORTH", "DE_SOUTH", "DE_EAST", "DE_WEST"]
    rows = []
    experiment_start = dates[len(dates) // 2]

    for market_index, market in enumerate(markets):
        treatment = market_index < 2

        for date in dates:
            baseline = 110 + market_index * 12
            trend = (date - dates[0]).days * 0.08
            noise = rng.normal(0, 9)

            treatment_effect = (
                12
                if treatment and date >= experiment_start
                else 0
            )

            additional_spend = (
                90
                if treatment and date >= experiment_start
                else 0
            )

            rows.append(
                {
                    "date": date.date().isoformat(),
                    "market": market,
                    "treatment_group": int(treatment),
                    "experiment_period": int(date >= experiment_start),
                    "marketing_spend_eur": round(
                        220 + market_index * 15 + additional_spend,
                        2,
                    ),
                    "new_paying_customers": max(
                        0,
                        int(
                            round(
                                baseline
                                + trend
                                + treatment_effect
                                + noise
                            )
                        ),
                    ),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    rng = np.random.default_rng(SEED)
    dates = pd.date_range(START_DATE, END_DATE, freq="D")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    campaigns = generate_campaigns(rng)
    spend = generate_spend(campaigns, dates, rng)

    users, events, subscriptions = generate_users_and_events(
        spend,
        campaigns,
        rng,
    )

    crm = generate_crm_experiments(users, rng)
    geo = generate_geo_experiment(dates, rng)

    datasets = {
        "campaigns.csv": campaigns,
        "ad_spend.csv": spend,
        "users.csv": users,
        "app_events.csv": events,
        "subscriptions.csv": subscriptions,
        "crm_experiments.csv": crm,
        "geo_experiments.csv": geo,
    }

    print("PULSEGROWTH SYNTHETIC DATA GENERATION")
    print("=" * 60)

    for filename, dataframe in datasets.items():
        dataframe.to_csv(OUTPUT_DIR / filename, index=False)
        print(f"{filename:<26} {len(dataframe):>10,} rows")

    print("=" * 60)
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    print(f"Random seed: {SEED}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("Synthetic data generation completed.")


if __name__ == "__main__":
    main()
