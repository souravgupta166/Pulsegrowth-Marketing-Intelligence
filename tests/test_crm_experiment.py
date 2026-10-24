
import pytest

from src.analytics.analyze_crm_experiment import analyse


def test_equal_conversion_rates_have_zero_lift():
    result = analyse(
        control_n=1000,
        control_x=100,
        treatment_n=1000,
        treatment_x=100,
    )

    assert result["absolute_lift"] == pytest.approx(0.0)
    assert result["relative_lift"] == pytest.approx(0.0)
    assert result["p_value"] == pytest.approx(1.0)
    assert result["statistically_significant"] is False


def test_positive_treatment_effect_is_detected():
    result = analyse(
        control_n=10000,
        control_x=900,
        treatment_n=10000,
        treatment_x=1200,
    )

    assert result["absolute_lift"] == pytest.approx(0.03)
    assert result["relative_lift"] == pytest.approx(1 / 3)
    assert result["ci_lower"] > 0
    assert result["p_value"] < 0.05
    assert result["statistically_significant"] is True


def test_confidence_interval_contains_zero_for_small_difference():
    result = analyse(
        control_n=100,
        control_x=10,
        treatment_n=100,
        treatment_x=11,
    )

    assert result["ci_lower"] <= 0 <= result["ci_upper"]
    assert result["statistically_significant"] is False


def test_zero_control_conversion_has_no_relative_lift():
    result = analyse(
        control_n=1000,
        control_x=0,
        treatment_n=1000,
        treatment_x=50,
    )

    assert result["control_rate"] == 0
    assert result["treatment_rate"] == pytest.approx(0.05)
    assert result["relative_lift"] is None


def test_zero_sized_group_raises_error():
    with pytest.raises(ValueError):
        analyse(
            control_n=0,
            control_x=0,
            treatment_n=100,
            treatment_x=10,
        )


def test_conversions_cannot_exceed_assigned_users():
    with pytest.raises(ValueError):
        analyse(
            control_n=100,
            control_x=101,
            treatment_n=100,
            treatment_x=10,
        )
