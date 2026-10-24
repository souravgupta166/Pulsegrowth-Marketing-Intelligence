
WITH experiment_summary AS (
    SELECT
        experiment_id,
        segment,
        variant,
        COUNT(*) AS assigned_users,
        SUM(converted_within_7d) AS conversions,
        AVG(converted_within_7d::DOUBLE) AS conversion_rate
    FROM {{ ref('stg_crm_experiments') }}
    GROUP BY experiment_id, segment, variant
),

overall_summary AS (
    SELECT
        experiment_id,
        'ALL_SEGMENTS' AS segment,
        variant,
        COUNT(*) AS assigned_users,
        SUM(converted_within_7d) AS conversions,
        AVG(converted_within_7d::DOUBLE) AS conversion_rate
    FROM {{ ref('stg_crm_experiments') }}
    GROUP BY experiment_id, variant
)

SELECT * FROM experiment_summary
UNION ALL
SELECT * FROM overall_summary
