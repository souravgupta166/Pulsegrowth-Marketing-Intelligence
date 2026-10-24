
import numpy as np
import pandas as pd

from src.ingestion.generate_data import (
    generate_campaigns,
    generate_crm_experiments,
    generate_geo_experiment,
    generate_spend,
)


def test_campaign_count_and_uniqueness():
    campaigns = generate_campaigns(np.random.default_rng(42))

    assert len(campaigns) == 16
    assert campaigns["campaign_id"].is_unique
    assert campaigns["channel"].nunique() == 4


def test_spend_has_valid_metrics():
    rng = np.random.default_rng(42)
    campaigns = generate_campaigns(rng)
    dates = pd.date_range("2026-09-01", periods=3, freq="D")

    spend = generate_spend(campaigns, dates, rng)

    assert len(spend) == len(campaigns) * len(dates)
    assert (spend["spend_eur"] >= 0).all()
    assert (spend["impressions"] >= spend["clicks"]).all()
    assert (spend["clicks"] >= 0).all()


def test_crm_experiment_has_valid_assignments():
    users = pd.DataFrame(
        {
            "user_id": [f"user_{i}" for i in range(100)],
            "install_date": ["2026-09-01"] * 100,
        }
    )

    result = generate_crm_experiments(
        users,
        np.random.default_rng(42),
    )

    assert result["user_id"].is_unique
    assert set(result["variant"]).issubset({"control", "treatment"})
    assert set(result["converted_within_7d"]).issubset({0, 1})


def test_geo_experiment_flags_are_binary():
    dates = pd.date_range("2026-09-01", periods=10, freq="D")

    result = generate_geo_experiment(
        dates,
        np.random.default_rng(42),
    )

    assert len(result) == 40
    assert set(result["treatment_group"]).issubset({0, 1})
    assert set(result["experiment_period"]).issubset({0, 1})
