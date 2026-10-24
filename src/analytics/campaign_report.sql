
-- PulseGrowth campaign decision report.
-- Run against data/processed/pulsegrowth.duckdb.

SELECT
    channel,
    campaign_name,
    ROUND(spend_eur, 2) AS spend_eur,
    attributed_installs,
    paying_customers,
    ROUND(customer_acquisition_cost_eur, 2) AS cac_eur,
    ROUND(attributed_revenue_eur, 2) AS attributed_revenue_eur,
    ROUND(attributed_roas, 3) AS attributed_roas,
    ROUND(100 * install_to_payer_rate, 2) AS install_to_payer_pct
FROM mart_campaign_performance
ORDER BY attributed_roas DESC NULLS LAST;
