
SELECT
    user_id,
    CAST(install_date AS DATE) AS install_date,
    campaign_id,
    channel,
    country,
    platform
FROM {{ source('pulsegrowth', 'fct_users') }}
