
SELECT
    transaction_id,
    user_id,
    CAST(transaction_date AS DATE) AS transaction_date,
    CAST(revenue_eur AS DOUBLE) AS revenue_eur,
    transaction_type
FROM {{ source('pulsegrowth', 'fct_subscriptions') }}
