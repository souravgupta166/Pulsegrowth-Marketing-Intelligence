
WITH spend AS (
    SELECT
        campaign_id,
        channel,
        SUM(spend_eur) AS spend_eur,
        SUM(impressions) AS impressions,
        SUM(clicks) AS clicks
    FROM {{ ref('stg_ad_spend') }}
    GROUP BY campaign_id, channel
),

installs AS (
    SELECT
        campaign_id,
        COUNT(*) AS attributed_installs
    FROM {{ ref('stg_users') }}
    WHERE campaign_id IS NOT NULL
    GROUP BY campaign_id
),

paying_users AS (
    SELECT
        u.campaign_id,
        COUNT(DISTINCT u.user_id) AS paying_customers
    FROM {{ ref('stg_users') }} u
    INNER JOIN (
        SELECT DISTINCT user_id
        FROM {{ ref('stg_subscriptions') }}
    ) s USING (user_id)
    WHERE u.campaign_id IS NOT NULL
    GROUP BY u.campaign_id
),

revenue AS (
    SELECT
        u.campaign_id,
        SUM(s.revenue_eur) AS attributed_revenue_eur
    FROM {{ ref('stg_users') }} u
    INNER JOIN {{ ref('stg_subscriptions') }} s USING (user_id)
    WHERE u.campaign_id IS NOT NULL
    GROUP BY u.campaign_id
)

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.campaign_theme,
    COALESCE(s.spend_eur, 0) AS spend_eur,
    COALESCE(s.impressions, 0) AS impressions,
    COALESCE(s.clicks, 0) AS clicks,
    COALESCE(i.attributed_installs, 0) AS attributed_installs,
    COALESCE(p.paying_customers, 0) AS paying_customers,
    COALESCE(r.attributed_revenue_eur, 0) AS attributed_revenue_eur,

    COALESCE(s.spend_eur, 0)
        / NULLIF(i.attributed_installs, 0) AS cost_per_install_eur,

    COALESCE(s.spend_eur, 0)
        / NULLIF(p.paying_customers, 0) AS cac_eur,

    COALESCE(r.attributed_revenue_eur, 0)
        / NULLIF(s.spend_eur, 0) AS attributed_roas

FROM {{ source('pulsegrowth', 'dim_campaigns') }} c
LEFT JOIN spend s USING (campaign_id)
LEFT JOIN installs i USING (campaign_id)
LEFT JOIN paying_users p USING (campaign_id)
LEFT JOIN revenue r USING (campaign_id)
