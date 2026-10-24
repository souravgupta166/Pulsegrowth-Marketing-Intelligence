SELECT
    experiment_id,
    user_id,
    segment,
    variant,
    CAST(assigned_date AS DATE) AS assigned_date,
    CAST(converted_within_7d AS INTEGER) AS converted_within_7d
FROM {{ source('pulsegrowth', 'fct_crm_experiments') }}