
SELECT
    CAST(date AS DATE) AS spend_date,
    campaign_id,
    channel,
    CAST(spend_eur AS DOUBLE) AS spend_eur,
    CAST(impressions AS BIGINT) AS impressions,
    CAST(clicks AS BIGINT) AS clicks
FROM {{ source('pulsegrowth', 'fct_ad_spend') }}
