
# PulseGrowth Data Dictionary

## Data provenance

All datasets are synthetically generated for portfolio development.
They do not represent real users, a real health-tech company, or actual
advertising-platform exports.

## campaigns.csv

One row per campaign.

| Column | Meaning |
|---|---|
| campaign_id | Unique campaign identifier |
| campaign_name | Descriptive campaign name |
| channel | Acquisition channel |
| campaign_theme | Campaign creative theme |
| daily_budget_eur | Simulated daily budget |
| target_country | Target market |

## ad_spend.csv

One row per campaign per date.

| Column | Meaning |
|---|---|
| date | Reporting date |
| campaign_id | Campaign identifier |
| channel | Acquisition channel |
| spend_eur | Simulated advertising spend |
| impressions | Simulated impressions |
| clicks | Simulated clicks |

## users.csv

One row per acquired user.

| Column | Meaning |
|---|---|
| user_id | Unique synthetic user |
| install_date | First install date |
| campaign_id | Campaign identifier; null if unattributed |
| channel | Acquisition source |
| country | Synthetic target market |
| platform | iOS or Android |

## app_events.csv

One row per simulated app event.

| Column | Meaning |
|---|---|
| event_id | Unique event identifier |
| user_id | User who generated the event |
| event_date | Event date |
| event_name | app_open or session_start |

## subscriptions.csv

One row per initial subscription transaction.

| Column | Meaning |
|---|---|
| transaction_id | Unique transaction identifier |
| user_id | Purchasing user |
| transaction_date | Transaction date |
| revenue_eur | Simulated gross transaction amount |
| transaction_type | Transaction classification |

The dataset currently models initial transactions only. It does not model
renewals, refunds, taxes, platform fees, or contribution margin.

## crm_experiments.csv

One row per user assigned to the simulated CRM experiment.

| Column | Meaning |
|---|---|
| experiment_id | Experiment identifier |
| user_id | Assigned user |
| segment | Simulated user segment |
| variant | Control or treatment |
| assigned_date | Assignment date |
| converted_within_7d | Simulated binary outcome |

The treatment effect is deliberately simulated. Statistical results from
this dataset are not empirical evidence about a real CRM campaign.

## geo_experiments.csv

One row per market per date.

| Column | Meaning |
|---|---|
| date | Observation date |
| market | Synthetic geographic market |
| treatment_group | 1 for treatment markets, 0 otherwise |
| experiment_period | 1 for the post-treatment period |
| marketing_spend_eur | Simulated market-level spend |
| new_paying_customers | Simulated daily outcome |

Only four markets are represented. Treatment assignment is not randomised.
Geo-lift results are suitable for learning and testing, not causal claims
about a real advertising intervention.
