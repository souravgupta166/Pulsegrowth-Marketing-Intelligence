# PulseGrowth — Marketing Intelligence Platform

> **Turning marketing data into better growth decisions.**
>
> A portfolio project demonstrating marketing analytics, campaign performance measurement, customer acquisition efficiency, cohort retention, experimentation, and budget allocation through an interactive Streamlit dashboard.

**Tech stack:** Python · SQL · DuckDB · dbt · Pandas · SciPy/statistical analysis · Streamlit · Pytest

**Project type:** End-to-end marketing analytics and decision-support platform

**Data:** Synthetic data generated for demonstration purposes

---

## Table of Contents

1. [Overview](#overview)
2. [Business Problem](#business-problem)
3. [Project Objectives](#project-objectives)
4. [Dashboard](#dashboard)
5. [Architecture](#architecture)
6. [Technology Stack](#technology-stack)
7. [Data Model](#data-model)
8. [Data Generation and Quality](#data-generation-and-quality)
9. [Marketing KPI Framework](#marketing-kpi-framework)
10. [Campaign Performance and Decision Logic](#campaign-performance-and-decision-logic)
11. [Attribution Coverage](#attribution-coverage)
12. [Cohort Retention Analysis](#cohort-retention-analysis)
13. [CRM Experimentation and Statistical Significance](#crm-experimentation-and-statistical-significance)
14. [Budget Simulator](#budget-simulator)
15. [dbt Transformation and Testing](#dbt-transformation-and-testing)
16. [Automated Testing](#automated-testing)
17. [How to Run the Project](#how-to-run-the-project)
18. [Project Structure](#project-structure)
19. [Key Analytical Findings](#key-analytical-findings)
20. [Limitations and Responsible Interpretation](#limitations-and-responsible-interpretation)
21. [Future Improvements](#future-improvements)
22. [Author](#author)

---

## 1. Overview

PulseGrowth is an interactive marketing intelligence platform designed to help a growth or marketing team understand campaign performance, evaluate customer acquisition efficiency, monitor retention, interpret CRM experiments, and explore potential budget allocation decisions.

Instead of looking at advertising metrics in isolation, the platform connects acquisition, conversion, retention, and experimentation into a single analytical workflow.

The project combines:

- A reproducible synthetic-data generation pipeline.
- Automated data-quality validation.
- A DuckDB analytical warehouse.
- SQL transformations managed through dbt.
- Python-based analytical workflows.
- An interactive Streamlit dashboard.
- Automated tests for core analytical logic.

The aim is to demonstrate how a Marketing Analyst can go beyond reporting numbers and use data to support practical business decisions.

**Important:** All campaign, customer, revenue, retention, and experiment data in this project are synthetic. The results demonstrate the analytical methodology and functionality of the platform, not the performance of a real business.

## 2. Business Problem

Marketing teams often work with information distributed across advertising platforms, product analytics, subscription systems, and customer relationship management tools.

This creates several analytical challenges.

### Acquisition efficiency

Which channels and campaigns acquire users at a lower cost? Are those users progressing towards paid conversion?

### Revenue efficiency

How much attributed revenue is associated with each unit of advertising spend? Which campaigns require further investigation?

### Customer retention

Are acquired users returning after installation? How does retention change across acquisition cohorts and channels?

### Experiment evaluation

Does a CRM treatment appear to improve conversion compared with a control group, and is the observed difference statistically distinguishable from zero?

### Budget allocation

How could a marketing team explore different spend scenarios while understanding the assumptions behind the resulting projections?

PulseGrowth addresses these questions through a unified data model and a dashboard designed around decision-making rather than disconnected metrics.

## 3. Project Objectives

The project was developed around six objectives:

1. **Create a reproducible data pipeline** that generates realistic marketing, user, subscription, event, and experiment datasets.
2. **Build a queryable analytical warehouse** using DuckDB and SQL.
3. **Standardise marketing KPIs** so that calculations are consistent and reproducible.
4. **Identify campaign-level performance differences** and translate them into review recommendations.
5. **Evaluate retention and experimentation** using cohort metrics and statistical analysis.
6. **Present the results through an interactive dashboard** that allows users to explore performance and potential decisions.

---

## 4. Dashboard

The PulseGrowth dashboard is built with Streamlit and uses a dark visual theme with lime and cyan accents.

**Application:** [Open the PulseGrowth dashboard](#)

Replace the placeholder link above with your deployed Streamlit URL when publishing the repository.

### Executive Overview

Provides a high-level view of marketing performance, including acquisition efficiency, attributed revenue, campaign performance, and key trends.

### Campaign Decision Centre

Allows users to compare campaign performance using spend, impressions, clicks, attributed installs, paying customers, customer acquisition cost, and attributed return on advertising spend.

### Cohort & Retention

Explores retention by acquisition month and channel, including Day 1, Day 7, and Day 30 retention metrics.

### Experimentation Lab

Presents CRM experiment outcomes, conversion rates, treatment-versus-control comparisons, and statistical significance.

### Budget Simulator

Provides an interactive environment for exploring alternative budget allocations using campaign performance data and explicit assumptions.

The simulator should be interpreted as a scenario-planning tool, not as a guarantee of future campaign outcomes.

---

## 5. Architecture

PulseGrowth follows a layered analytical architecture.

```text
Synthetic Data Generation
          |
          v
CSV Datasets
          |
          v
Data Quality Validation
          |
          v
DuckDB Analytical Warehouse
          |
          +----------------------+
          |                      |
          v                      v
SQL / dbt Transformations   Python Analytics
          |                      |
          +-----------+----------+
                      |
                      v
             Analytical Data Marts
                      |
                      v
             Streamlit Dashboard
                      |
                      v
          Marketing Decision Support
```

### Layer 1 — Data generation

Python generates the synthetic source datasets using a reproducible random seed.

### Layer 2 — Data quality

Validation checks test the generated data for expected structural and logical properties before analysis.

### Layer 3 — Warehouse

DuckDB stores the data locally and supports analytical SQL queries without requiring a separate database server.

### Layer 4 — Transformation

SQL and dbt organise source data into staging models and analytical marts.

### Layer 5 — Analytics

Python scripts calculate campaign decision metrics, attribution coverage, and experiment statistics.

### Layer 6 — Presentation

Streamlit brings the analytical outputs together in an interactive dashboard.

This separation makes the project easier to test, debug, extend, and reproduce.

---

## 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, analytics, validation, and application logic |
| Pandas | Data manipulation and analytical preparation |
| DuckDB | Local analytical database and SQL execution |
| SQL | Joins, aggregations, KPI calculations, and data transformations |
| dbt Core | Staging models, analytical marts, and data tests |
| Streamlit | Interactive dashboard |
| Plotly / Streamlit charts | Interactive analytical visualisations, where used |
| Pytest | Automated regression and logic testing |
| SciPy / statistical methods | Statistical evaluation of CRM experiment results |

The exact dependency versions should be taken from the project's dependency files when publishing the repository.

---

## 7. Data Model

The synthetic pipeline generates seven principal datasets.

| Dataset | Approximate rows | Purpose |
|---|---:|---|
| `campaigns.csv` | 16 | Campaign definitions and budget metadata |
| `ad_spend.csv` | 2,880 | Daily advertising spend, impressions, and clicks |
| `users.csv` | 659,938 | User acquisition and attribution information |
| `app_events.csv` | 2,743,172 | User activity events |
| `subscriptions.csv` | 58,404 | Subscription and revenue transactions |
| `crm_experiments.csv` | 395,963 | User-level CRM experiment assignments and outcomes |
| `geo_experiments.csv` | 720 | Illustrative market-level experiment data |

The generated data cover **4 April 2026 to 30 September 2026**, using seed `42`.

### Warehouse tables

The DuckDB warehouse contains source-oriented tables such as:

- `main.dim_campaigns`
- `main.fct_ad_spend`
- `main.fct_users`
- `main.fct_app_events`
- `main.fct_subscriptions`
- `main.fct_crm_experiments`
- `main.fct_geo_experiments`

It also contains analytical tables, including:

- `main.mart_campaign_performance`
- `main.mart_daily_campaign_performance`
- `main.mart_cohort_retention`
- `analytics.mart_campaign_performance`
- `analytics.mart_crm_experiment_results`

The `analytics` schema includes dbt staging models and transformed analytical outputs. The `main` schema contains the broader warehouse tables and marts.

### Important modelling distinction

The warehouse includes both `main.mart_campaign_performance` and `analytics.mart_campaign_performance`. Their schemas are not identical.

For example, the `main` mart includes CTR, CPC, cost per attributed install, and install-to-payer conversion, while the dbt mart includes CPI, CAC, and attributed ROAS.

These should be documented and maintained as distinct models until their definitions and intended uses have been explicitly reconciled.

---

## 8. Data Generation and Quality

The project uses synthetic data to simulate the types of relationships found in a subscription-oriented digital product.

The generation process includes:

- Advertising campaigns across Google Ads, Meta Ads, TikTok Ads, and Apple Search Ads.
- Daily advertising spend, impressions, and clicks.
- User installs and campaign attribution.
- Product activity events.
- Subscription transactions.
- CRM treatment and control assignments.
- Illustrative geographic experiment observations.

The generator also includes unattributed users, allowing the project to demonstrate the impact of incomplete attribution.

### Reproducibility

A fixed random seed of `42` supports repeatable data generation when the same code and environment are used.

### Validation

The data validation script reported **27 out of 27 checks passing**.

This establishes that the generated datasets passed the implemented validation rules. It does not independently establish that every business assumption is realistic or that the data represent a real marketing environment.

---

## 9. Marketing KPI Framework

The platform uses a common set of marketing performance indicators.

Let:

- \(S\) = advertising spend.
- \(I\) = impressions.
- \(C\) = clicks.
- \(A\) = attributed installs.
- \(P\) = attributed paying customers.
- \(R\) = revenue attributed to the campaign.

### 9.1 Click-through rate (CTR)

Measures the proportion of impressions that generated clicks.

\[
CTR=\frac{C}{I}\times100
\]

**Interpretation:** A higher CTR indicates that a greater proportion of impressions generated clicks. It does not, by itself, prove that the campaign acquires valuable customers.

### 9.2 Cost per click (CPC)

Measures the average advertising cost per click.

\[
CPC=\frac{S}{C}
\]

**Interpretation:** Lower CPC can improve acquisition efficiency, but only when downstream conversion quality remains acceptable.

### 9.3 Cost per install (CPI)

Measures advertising spend per attributed install.

\[
CPI=\frac{S}{A}
\]

**Interpretation:** CPI is useful for comparing acquisition costs, but it does not measure how many acquired users become paying customers.

### 9.4 Customer acquisition cost (CAC)

The campaign-level calculation used in this project is:

\[
CAC=\frac{S}{P}
\]

Here, \(P\) represents the paying customers attributed to the campaign.

This is an advertising-spend-based acquisition cost. It is not necessarily the same as fully loaded business CAC, which may include agency fees, salaries, incentives, creative production, and other acquisition costs.

### 9.5 Install-to-payer conversion rate

\[
\text{Install-to-payer rate}
=\frac{P}{A}\times100
\]

**Interpretation:** This helps distinguish campaigns that generate many installs from campaigns that generate paying customers.

### 9.6 Attributed revenue

Attributed revenue is the revenue associated with users assigned to a campaign under the project's attribution logic.

It is not automatically incremental revenue. Revenue could have occurred without the advertising campaign.

### 9.7 Attributed return on advertising spend (ROAS)

\[
\text{Attributed ROAS}=\frac{R}{S}
\]

For example, a ROAS of \(0.60\times\) means that the attributed revenue recorded by the model is €0.60 for each €1 of advertising spend.

It does **not** mean the business earned €0.60 in profit, and it does not prove that the advertising caused the revenue.

### Calculation safeguards

Ratios require sensible handling of zero denominators. When spend, impressions, clicks, installs, or paying customers are zero, the implementation should return a null or clearly defined fallback rather than presenting an invalid ratio as a real result.

Metric definitions should also be consistent across the dashboard, Python scripts, and dbt models.

---

## 10. Campaign Performance and Decision Logic

The campaign decision table combines acquisition, engagement, conversion, and attributed revenue metrics.

The resulting dataset includes:

- Performance rank.
- Campaign and channel.
- Spend and impressions.
- Clicks and CTR.
- Attributed installs and CPI.
- Paying customers and CAC.
- Install-to-payer conversion.
- Attributed revenue and revenue per install.
- Attributed ROAS.
- A recommendation label.

### Decision framework

The project's initial recommendation logic uses ROAS and engagement efficiency as screening signals.

| Condition | Initial interpretation |
|---|---|
| Attributed ROAS at or above 1.0x | Promising for further evaluation |
| Attributed ROAS below 0.5x | Review campaign efficiency and economics |
| Other campaigns | Monitor performance and examine supporting metrics |

These are **portfolio-project screening thresholds**, not universal marketing benchmarks.

A campaign with ROAS above 1.0x is not necessarily profitable. Profitability depends on margins, refunds, retention, payment fees, operating costs, and the period over which revenue is measured.

Similarly, a campaign with low initial ROAS may need more time to mature if subscription revenue accumulates over time.

### Why use multiple metrics?

Optimising only for CPI may favour campaigns that acquire large numbers of low-intent users.

Considering CPI alongside CAC, conversion, and attributed ROAS provides a more complete view of acquisition efficiency.

The decision table is intended to help prioritise investigation, not to replace business judgement or causal evaluation.

---

## 11. Attribution Coverage

The attribution analysis compares the total user population with the users assigned to identifiable acquisition channels.

The synthetic output reported:

| Attribution category | Users |
|---|---:|
| Google Ads | 186,812 |
| Meta Ads | 165,574 |
| Apple Search Ads | 134,996 |
| TikTok Ads | 120,039 |
| Unattributed | 52,517 |
| **Total** | **659,938** |

Attributed users totalled 607,421.

Overall attribution coverage is calculated as:

\[
\text{Coverage}=
\frac{\text{Attributed users}}
{\text{Total users}}\times100
\]

Using the generated results:

\[
\text{Coverage}=
\frac{607421}{659938}\times100
\approx92.04\%
\]

Therefore, approximately 92.04% of generated users were assigned to an acquisition channel, while approximately 7.96% were unattributed.

### Why this matters

Incomplete attribution can affect:

- Channel comparisons.
- Campaign-level CAC.
- Reported attributed revenue.
- Budget allocation decisions.
- Confidence in marketing performance reporting.

Coverage is a data-completeness measure. It does not tell us whether the attribution assignments are causally correct or whether one channel generated incremental growth.

---

## 12. Cohort Retention Analysis

The cohort analysis groups users by acquisition month and channel, then examines their subsequent activity.

The warehouse's `main.mart_cohort_retention` model contains:

- `cohort_month`
- `channel`
- `cohort_users`
- `d1_eligible_users`
- `d1_retained_users`
- `d7_eligible_users`
- `d7_retained_users`
- `d30_eligible_users`
- `d30_retained_users`
- `d1_retention_rate`
- `d7_retention_rate`
- `d30_retention_rate`

### 12.1 Day 1 retention

\[
R_{D1}=
\frac{\text{D1 retained users}}
{\text{D1 eligible users}}\times100
\]

### 12.2 Day 7 retention

\[
R_{D7}=
\frac{\text{D7 retained users}}
{\text{D7 eligible users}}\times100
\]

### 12.3 Day 30 retention

\[
R_{D30}=
\frac{\text{D30 retained users}}
{\text{D30 eligible users}}\times100
\]

The denominator should include only users with sufficient observation time to reach the relevant retention milestone.

For example, a user who installed one day before the dataset cutoff cannot yet be evaluated for Day 30 retention.

### Weighted aggregation

When combining channels or cohorts, overall retention should be calculated from the underlying retained and eligible counts:

\[
R_{\text{overall}}=
\frac{\sum_i \text{retained}_i}
{\sum_i \text{eligible}_i}\times100
\]

This is preferable to taking a simple average of percentages because cohorts can have different sizes.

### Interpretation

The dashboard allows the user to compare retention across acquisition months and channels.

A channel with strong acquisition metrics but weak retention may be attracting users who do not remain active. A channel with more modest install volume but stronger downstream retention may warrant further investigation.

### Retention maturity audit

The platform includes a diagnostic for checking cohort counts and eligibility.

This matters because retention rates are only meaningful when users have had enough time to reach the relevant milestone. The generated dataset ends on 30 September 2026, so recent cohorts require particular attention.

The dashboard's maturity diagnostic is a warning mechanism. It should not be treated as proof that a cohort calculation is wrong; the underlying SQL eligibility logic must be checked against individual install and event dates.

---

## 13. CRM Experimentation and Statistical Significance

The CRM experiment analysis compares conversion outcomes between treatment and control groups.

The generated dataset includes an experiment assignment, customer segment, and an indicator of whether the user converted within seven days.

### 13.1 Conversion rate

For each experiment group:

\[
p=\frac{x}{n}
\]

where:

- \(x\) is the number of conversions.
- \(n\) is the number of assigned users.

### 13.2 Absolute conversion lift

\[
\Delta=p_T-p_C
\]

where \(p_T\) is the treatment conversion rate and \(p_C\) is the control conversion rate.

Absolute lift is usually reported in percentage points.

### 13.3 Relative conversion lift

\[
\text{Relative lift}=
\frac{p_T-p_C}{p_C}\times100
\]

Relative lift expresses the difference relative to the control conversion rate. It should be interpreted alongside the absolute difference.

### 13.4 Statistical significance

The analysis evaluates whether the observed treatment-control difference is statistically distinguishable from zero.

The significance level used by the analysis is:

\[
\alpha=0.05
\]

For a two-sided test, the hypotheses are:

\[
H_0:p_T-p_C=0
\]

\[
H_1:p_T-p_C\neq0
\]

If the p-value is below 0.05, the result is classified as statistically significant under this testing framework.

Statistical significance does not measure the size or business value of an effect. It also does not establish causality if experiment assignment, data quality, or the analysis assumptions are compromised.

### 13.5 Confidence interval

A 95% confidence interval describes the uncertainty around the estimated difference in conversion rates under the selected statistical method.

An interval excluding zero is consistent with statistical significance for the corresponding two-sided test at the 5% level, subject to the assumptions of the method.

### Results from the generated dataset

The current synthetic output reported:

| Metric | Control | Treatment |
|---|---:|---:|
| Assigned users | 198,038 | 197,925 |
| Conversions | 18,211 | 23,218 |
| Conversion rate | 9.20% | 11.73% |

The reported absolute lift was approximately **+2.53 percentage points**, with relative lift of approximately **+27.57%**.

The reported 95% confidence interval for the absolute difference was approximately **+2.34 to +2.73 percentage points**. The p-value was reported as below the display precision of six decimal places.

These results are intentionally generated by the synthetic experiment process. They demonstrate how the analysis works; they are not evidence of a real CRM campaign's effectiveness.

### Segment analysis

The experiment script also reports outcomes for customer segments, including new, inactive, and trial users.

Segment-level findings should be interpreted with care because testing multiple segments increases the chance of false-positive results. A production implementation should predefine primary outcomes and consider multiple-comparison adjustments where appropriate.

---

## 14. Budget Simulator

The Budget Simulator supports exploratory budget planning based on campaign performance.

A scenario simulator can help answer questions such as:

- What happens if the budget allocation changes?
- How much spend is assigned to each campaign?
- What historical acquisition or revenue efficiency would imply under a proposed allocation?
- Which assumptions have the greatest influence on the projection?

### Core scenario logic

For a simple spend allocation scenario, let:

- \(B_i\) be the proposed budget for campaign \(i\).
- \(r_i\) be the selected historical performance ratio for campaign \(i\).

A basic projection can be expressed as:

\[
\widehat{Y}_i=B_i\times r_i
\]

For example, if the selected ratio is historical attributed revenue divided by historical spend, then:

\[
\widehat{R}_i=B_i\times
\frac{R_i}{S_i}
\]

This is a **historical-rate scenario**, not a forecast with guaranteed outcomes. The formula assumes the historical ratio remains stable as spend changes.

The exact calculations, constraints, and controls implemented in the current simulator should be documented against the final `app.py` code before describing the tool as an optimiser.

### Important limitations

Real campaigns may experience diminishing returns, audience saturation, changes in auction prices, seasonal effects, and interactions between channels.

A more advanced budget optimiser would incorporate marginal performance curves, spend limits, uncertainty, and an explicit business objective.

---

## 15. dbt Transformation and Testing

The project uses dbt Core with the DuckDB adapter to organise analytical transformations.

The dbt project includes staging models such as:

- `stg_ad_spend`
- `stg_crm_experiments`
- `stg_subscriptions`
- `stg_users`

It also includes analytical marts such as:

- `mart_campaign_performance`
- `mart_crm_experiment_results`

### Why dbt?

Using dbt makes the transformation layer easier to maintain by separating SQL logic into named, reusable models.

It also supports:

- Declared sources.
- Model-level data tests.
- Documentation generation.
- Repeatable transformation runs.
- More transparent lineage between source tables and analytical outputs.

### Example campaign mart logic

At a high level, campaign performance combines spend, user acquisition, subscription outcomes, and campaign metadata.

Before aggregating these sources, each input should be reduced to an appropriate grain. Otherwise, joining daily spend to multiple user events or subscription transactions can duplicate values and inflate metrics.

A robust transformation therefore needs to verify join keys, aggregation grain, attribution rules, and revenue definitions.

The exact SQL should remain the source of truth for the production formulas; the formulas in this README describe the intended analytical definitions.

---

## 16. Automated Testing

The project uses Pytest to validate important analytical behaviour.

The latest reported full test run completed with:

**15 tests passed.**

The reported test groups include:

- Data-related tests.
- CRM experiment analysis tests.
- Campaign decision-table tests.

The synthetic-data validation script also reported 27 successful data-quality checks.

### What these tests demonstrate

Automated tests help protect against regressions in calculations, expected data behaviour, and recommendation logic.

Passing tests do not automatically guarantee that all business definitions are correct. Analytical validation should also compare outputs with independently calculated values and check the assumptions behind each metric.

---

## 17. How to Run the Project

### Prerequisites

- Python 3.12.
- Git.
- A Windows PowerShell terminal or a compatible shell.
- The project dependency files.

The following commands assume the repository uses the `.venv` virtual environment and that the relevant scripts are available at the documented paths.

### Step 1 — Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd pulsegrowth-marketing-intelligence
```

Replace the placeholder with the actual repository URL.

### Step 2 — Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

If the repository includes a `requirements.txt` file:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependencies are managed differently, follow the repository's actual dependency configuration.

### Step 4 — Generate synthetic data

```powershell
python src/ingestion/generate_data.py
```

This should generate the source CSV files used by the analytical pipeline.

### Step 5 — Validate the data

```powershell
python src/ingestion/validate_data.py
```

Review the output and resolve validation failures before continuing.

### Step 6 — Build the warehouse

Run the repository's warehouse build or data-loading workflow to populate the DuckDB database and required analytical tables.

The exact command depends on the current implementation; document the actual command from the project scripts before publishing this section.

### Step 7 — Run dbt transformations

From the directory containing the dbt project configuration:

```powershell
dbt debug
dbt run
dbt test
```

If the dbt project is in a subdirectory, first navigate to that directory or specify it with the appropriate `--project-dir` and profile options.

### Step 8 — Run automated tests

```powershell
python -m pytest -v
```

### Step 9 — Launch the dashboard

From the repository root:

```powershell
python -m streamlit run app.py
```

Streamlit will provide a local URL for the dashboard.

**Reproducibility note:** The repository README should list the exact command sequence needed to build the database from a fresh clone. A pre-existing local DuckDB file should not be a hidden prerequisite.

---

## 18. Project Structure

The following is a conceptual layout based on the project components. Verify the actual file tree before publishing it as an exact directory listing.

```text
pulsegrowth-marketing-intelligence/
│
├── app.py
├── dbt_project/
│   └── models/
│       ├── staging/
│       └── marts/
│
├── src/
│   ├── ingestion/
│   │   ├── generate_data.py
│   │   └── validate_data.py
│   │
│   └── analytics/
│       ├── analyze_crm_experiment.py
│       ├── attribution_coverage.py
│       └── build_campaign_decision_table.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── tests/
│   ├── test_data.py
│   ├── test_crm_experiment.py
│   └── test_campaign_decision_table.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

Generated databases and large datasets may be excluded from version control when they can be reproducibly rebuilt. The README should explain how to recreate them.

---

## 19. Key Analytical Findings

The current synthetic run demonstrates several useful analytical patterns.

### Attribution completeness

The attribution workflow reported approximately **92.04% coverage**, with 52,517 users remaining unattributed.

This demonstrates why attribution completeness should be checked before relying on channel comparisons.

### Campaign efficiency

The synthetic campaign decision table showed differences in attributed ROAS and acquisition costs across channels. Apple Search Ads campaigns had higher attributed ROAS in the current generated output than the other represented channels.

This is a result of the generated data and modelling assumptions, not a real-world channel benchmark.

### CRM experiment

The synthetic treatment group showed a higher seven-day conversion rate than the control group. The analysis reports absolute lift, relative lift, a confidence interval, and statistical significance.

### Cohort retention

The retention dashboard compares Day 1, Day 7, and Day 30 outcomes across cohorts and channels. It also highlights the importance of checking observation maturity before interpreting retention rates.

### Overall learning

The project illustrates that acquisition efficiency, attributed revenue, retention, attribution completeness, and experimentation provide different kinds of evidence.

A strong marketing decision should consider these signals together rather than treating any single KPI as sufficient.

---

## 20. Limitations and Responsible Interpretation

PulseGrowth is a demonstration project, and several limitations are important.

### Synthetic data

The data were generated programmatically. They do not represent real users, real advertising accounts, or verified company performance.

### Attribution is not causality

Attributed revenue and attributed ROAS measure results under the chosen attribution logic. They do not establish incremental revenue generated by advertising.

### Historical performance is not a forecast

Campaign efficiency can change as budgets, audiences, competition, creative assets, and market conditions change.

### CAC is narrowly defined

The campaign-level CAC calculation uses advertising spend divided by attributed paying customers. It does not include every cost that may be relevant to fully loaded acquisition economics.

### Retention requires maturity checks

Users need enough elapsed time to become eligible for Day 1, Day 7, or Day 30 measurements. Eligibility must be based on individual observation windows, not assumed from the cohort label alone.

### Experiments depend on design quality

Statistical significance is meaningful only when the assignment mechanism, outcome definitions, observation windows, and test assumptions are appropriate.

### Geographic experiment data

The geographic experiment dataset is illustrative. It should not be presented as a validated causal analysis unless the design, treatment assignment, comparison period, and estimation method are explicitly implemented and checked.

---

## 21. Future Improvements

Potential next steps include:

1. **Incrementality measurement:** Add a carefully validated geographic or user-level causal analysis.
2. **Lifetime value:** Estimate customer lifetime value using subscription history and explicit assumptions.
3. **Budget optimisation:** Model diminishing returns and optimise allocations under campaign-level constraints.
4. **Attribution diagnostics:** Add checks for missing identifiers, unattributed users, and conflicting channel assignments.
5. **Retention maturity:** Validate eligibility at the individual-user level and test boundary dates.
6. **Data contracts:** Add stronger schema, uniqueness, referential-integrity, and reconciliation tests.
7. **Metric governance:** Standardise KPI definitions across the Python, SQL, dbt, and dashboard layers.
8. **Deployment:** Document a clean, reproducible deployment process and keep generated secrets and local data out of version control.
9. **Monitoring:** Add checks for unexpected changes in data volumes, campaign metrics, and pipeline execution.
10. **Visual storytelling:** Include a small number of annotated charts that connect findings to specific business decisions.

---

## 22. Author

Built as a hands-on portfolio project to demonstrate practical skills in marketing analytics, data engineering, SQL, experimentation, KPI design, and interactive business intelligence.

**GitHub:** <https://github.com/souravgupta166>

**LinkedIn:** <https://www.linkedin.com/in/sourav-gupta-7539a9217/?>

---

*PulseGrowth is an educational portfolio project. All reported business results are derived from synthetic data and should not be interpreted as real commercial outcomes.*
