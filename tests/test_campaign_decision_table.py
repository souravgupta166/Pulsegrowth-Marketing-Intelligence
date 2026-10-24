
import pandas as pd
import pytest

from src.analytics.build_campaign_decision_table import build_decision_table


@pytest.fixture
def sample_campaigns():
    return pd.DataFrame(
        [
            {
                "campaign_id": "C1",
                "campaign_name": "Campaign Alpha",
                "channel": "Search",
                "spend_eur": 100.0,
                "impressions": 10000,
                "clicks": 500,
                "attributed_installs": 100,
                "paying_customers": 20,
                "attributed_revenue_eur": 150.0,
            },
            {
                "campaign_id": "C2",
                "campaign_name": "Campaign Beta",
                "channel": "Social",
                "spend_eur": 200.0,
                "impressions": 20000,
                "clicks": 400,
                "attributed_installs": 100,
                "paying_customers": 10,
                "attributed_revenue_eur": 50.0,
            },
        ]
    )


def test_calculates_campaign_kpis(sample_campaigns):
    result = build_decision_table(sample_campaigns)
    alpha = result.loc[result["campaign_id"] == "C1"].iloc[0]

    assert alpha["click_through_rate"] == pytest.approx(0.05)
    assert alpha["cpi_eur"] == pytest.approx(1.0)
    assert alpha["cac_eur"] == pytest.approx(5.0)
    assert alpha["install_to_payer_conversion_rate"] == pytest.approx(0.20)
    assert alpha["revenue_per_install_eur"] == pytest.approx(1.50)
    assert alpha["attributed_roas"] == pytest.approx(1.50)


def test_campaigns_rank_by_roas(sample_campaigns):
    result = build_decision_table(sample_campaigns)

    assert result.iloc[0]["campaign_id"] == "C1"
    assert result.iloc[0]["performance_rank"] == 1
    assert result.iloc[1]["campaign_id"] == "C2"
    assert result.iloc[1]["performance_rank"] == 2


def test_zero_denominators_produce_missing_kpis():
    data = pd.DataFrame(
        [
            {
                "campaign_id": "C3",
                "campaign_name": "Zero Activity",
                "channel": "Test",
                "spend_eur": 0.0,
                "impressions": 0,
                "clicks": 0,
                "attributed_installs": 0,
                "paying_customers": 0,
                "attributed_revenue_eur": 0.0,
            }
        ]
    )

    result = build_decision_table(data)
    campaign = result.iloc[0]

    assert pd.isna(campaign["click_through_rate"])
    assert pd.isna(campaign["cpi_eur"])
    assert pd.isna(campaign["cac_eur"])
    assert pd.isna(campaign["attributed_roas"])
    assert campaign["recommendation"] == "Investigate spend data"


def test_duplicate_campaign_ids_are_rejected(sample_campaigns):
    duplicated = pd.concat(
        [sample_campaigns, sample_campaigns.iloc[[0]]],
        ignore_index=True,
    )

    with pytest.raises(ValueError, match="Campaign IDs are not unique"):
        build_decision_table(duplicated)


def test_negative_metrics_are_rejected(sample_campaigns):
    invalid = sample_campaigns.copy()
    invalid.loc[0, "spend_eur"] = -10

    with pytest.raises(ValueError, match="Negative values"):
        build_decision_table(invalid)
