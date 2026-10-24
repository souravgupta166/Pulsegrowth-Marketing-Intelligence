# PulseGrowth — Marketing Intelligence Platform

> **Turning marketing data into better growth decisions.**

PulseGrowth is an end-to-end marketing analytics and decision-support platform that connects campaign acquisition, conversion, revenue attribution, customer retention, CRM experimentation, and budget planning in one interactive application.

The project demonstrates how marketing data can be transformed into consistent KPIs, analytical data models, statistical evidence, and practical recommendations. It combines Python, SQL, DuckDB, dbt, statistical analysis, automated data validation, and Streamlit to create a reproducible marketing intelligence workflow.

**Live application:** [Open PulseGrowth Dashboard](https://pulsegrowth-marketing-intelligence-lrfpd5xacjdrrymdqzkqg9.streamlit.app/)

**GitHub repository:** [souravgupta166/Pulsegrowth-Marketing-Intelligence](https://github.com/souravgupta166/Pulsegrowth-Marketing-Intelligence)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Problem and Strategic Rationale](#2-business-problem-and-strategic-rationale)
3. [Business Objectives](#3-business-objectives)
4. [Live Dashboard and Features](#4-live-dashboard-and-features)
5. [Technology Stack](#5-technology-stack)
6. [System Architecture](#6-system-architecture)
7. [Data Generation and Dataset Design](#7-data-generation-and-dataset-design)
8. [Data Quality and Validation](#8-data-quality-and-validation)
9. [Data Warehouse and Data Model](#9-data-warehouse-and-data-model)
10. [Marketing KPI Framework and Mathematical Logic](#10-marketing-kpi-framework-and-mathematical-logic)
11. [Campaign Performance and Decision Strategy](#11-campaign-performance-and-decision-strategy)
12. [Attribution Coverage and Reliability](#12-attribution-coverage-and-reliability)
13. [Cohort Retention Analysis](#13-cohort-retention-analysis)
14. [CRM Experimentation and Statistical Analysis](#14-crm-experimentation-and-statistical-analysis)
15. [Budget Simulator and Scenario Planning](#15-budget-simulator-and-scenario-planning)
16. [dbt Transformation Strategy](#16-dbt-transformation-strategy)
17. [Testing and Analytical Quality Assurance](#17-testing-and-analytical-quality-assurance)
18. [Deployment and Performance Strategy](#18-deployment-and-performance-strategy)
19. [End-to-End Setup Instructions](#19-end-to-end-setup-instructions)
20. [Project Structure](#20-project-structure)
21. [Key Findings from the Synthetic Dataset](#21-key-findings-from-the-synthetic-dataset)
22. [Business Recommendations and Decision Framework](#22-business-recommendations-and-decision-framework)
23. [Limitations and Responsible Interpretation](#23-limitations-and-responsible-interpretation)
24. [Future Roadmap](#24-future-roadmap)
25. [Skills Demonstrated](#25-skills-demonstrated)
26. [Author](#26-author)

---

## 1. Executive Summary

Marketing teams need to understand more than how many impressions, clicks, or installs a campaign generates. They need to know whether acquisition spending translates into paying customers, whether those customers remain active, whether marketing interventions improve conversion, and how budgets could be allocated more effectively.

PulseGrowth addresses these questions through a unified analytical workflow.

The platform generates synthetic marketing and product data, validates the datasets, loads them into DuckDB, transforms them using SQL and dbt, calculates business KPIs, and presents the resulting insights through an interactive Streamlit dashboard.

The analytical workflow covers five connected areas:

- **Acquisition efficiency:** Measure campaign spend, impressions, clicks, installs, customer acquisition cost, and attributed revenue.
- **Campaign decision-making:** Compare channel and campaign performance and flag campaigns that need further investigation.
- **Retention intelligence:** Evaluate Day 1, Day 7, and Day 30 retention across acquisition cohorts.
- **Experimentation:** Compare CRM treatment and control groups using conversion rates, absolute lift, relative lift, confidence intervals, and statistical significance.
- **Budget planning:** Explore alternative spending allocations using historical campaign performance and transparent assumptions.

The project was built as a complete analytics workflow rather than a collection of independent charts. Each stage has a defined purpose, from data generation and validation to analytical transformation, business interpretation, and deployment.

### Project snapshot

| Component | Implementation |
|---|---|
| Application | Streamlit |
| Programming | Python |
| Analytical database | DuckDB |
| Transformation framework | dbt Core with dbt-duckdb |
| Data processing | Pandas and SQL |
| Statistical analysis | Hypothesis testing and confidence intervals |
| Data quality | Python validation scripts and dbt tests |
| Automated testing | Pytest |
| Data type | Synthetic marketing and product analytics data |
| Deployment | Streamlit Community Cloud |

**Important:** All users, campaigns, spending, conversions, subscriptions, revenue, and experiment outcomes are synthetic. The project demonstrates analytical methods and engineering practices; it does not report the actual performance of a real business.

---

## 2. Business Problem and Strategic Rationale

Marketing data often exists across advertising platforms, product analytics systems, subscription databases, and customer relationship management tools. When these sources are analysed separately, it becomes difficult to connect acquisition costs with downstream customer behaviour.

PulseGrowth was designed around five business problems.

### 2.1 Acquisition without downstream context

A campaign may generate a large number of inexpensive installs but attract users who never subscribe or return to the product.

Optimising exclusively for install volume can therefore lead to misleading conclusions.

**Strategic response:** Evaluate acquisition metrics alongside payer conversion, customer acquisition cost, attributed revenue, and retention.

### 2.2 Revenue attribution without causal evidence

Attributed revenue helps connect customers with campaigns under a chosen attribution rule. However, attribution does not establish that advertising caused the revenue.

Some customers might have converted without the campaign.

**Strategic response:** Separate descriptive campaign reporting from controlled experiments and incremental-effect measurement.

### 2.3 Inconsistent KPI definitions

Different reports can produce conflicting numbers when they use different aggregation levels, denominators, time windows, or definitions of a customer.

For example, averaging campaign-level CAC values does not generally produce the correct overall CAC.

**Strategic response:** Define metrics explicitly, calculate them from the correct underlying counts, and centralise reusable transformations in the analytical warehouse.

### 2.4 Retention metrics without maturity checks

A recently acquired customer cannot yet be evaluated for Day 30 retention. Treating that customer as a non-retained user would distort the analysis.

**Strategic response:** Separate eligible users from retained users and validate observation windows before interpreting retention rates.

### 2.5 Budget decisions based on incomplete evidence

Historical ROAS can help compare campaigns, but blindly moving budget towards the highest observed value can ignore audience saturation, uncertainty, customer quality, and changing marginal returns.

**Strategic response:** Use a transparent decision framework that combines multiple metrics, explicit assumptions, and scenario analysis.

### Strategic principle

PulseGrowth follows a simple principle:

> Measure acquisition, validate the data, understand customer behaviour, evaluate evidence, and only then consider a budget decision.

The objective is not to automate every decision. It is to make decisions more transparent, reproducible, and evidence-based.

---

## 3. Business Objectives

The project was developed around the following objectives:

1. Build a reproducible synthetic-data pipeline for marketing, user activity, subscriptions, and experiments.
2. Establish an analytical warehouse that supports repeatable SQL queries and aggregations.
3. Define a consistent KPI framework for acquisition, conversion, attributed revenue, and retention.
4. Identify campaign-level performance differences and produce review recommendations.
5. Evaluate customer retention using cohort-based metrics and eligibility checks.
6. Analyse CRM experiments using treatment-control comparisons and statistical methods.
7. Create an interactive budget-planning experience with explicit modelling assumptions.
8. Test data quality and core analytical logic before presenting results.
9. Deploy a compact analytical dataset so the dashboard does not need to load the entire raw warehouse at runtime.

These objectives cover both business analysis and the supporting data engineering required to deliver reliable analytical outputs.

---

## 4. Live Dashboard and Features

### Live application

**[Launch PulseGrowth — Marketing Intelligence](https://pulsegrowth-marketing-intelligence-lrfpd5xacjdrrymdqzkqg9.streamlit.app/)**

The application uses a dark interface with lime and cyan accents and is organised around five analytical workspaces.

### 4.1 Executive Overview

Purpose: provide a high-level view of marketing performance.

The overview brings together headline KPIs and campaign trends so that a user can understand the overall acquisition picture before exploring individual campaigns.

Business questions:

- How much has been spent on acquisition?
- How many users have been acquired?
- How efficiently does spending translate into attributed customers and revenue?
- Are campaign performance measures moving in the same direction?

The overview acts as the entry point for the broader decision workflow.

### 4.2 Campaign Decision Centre

Purpose: compare campaigns and identify where further investigation is needed.

The campaign analysis brings together advertising activity, acquisition, customer conversion, and attributed revenue.

Relevant metrics include:

- Advertising spend
- Impressions and clicks
- Click-through rate
- Cost per click
- Attributed installs
- Cost per install
- Paying customers
- Campaign-level customer acquisition cost
- Install-to-payer conversion
- Attributed revenue
- Attributed ROAS
- Campaign recommendation labels

The strategic focus is to distinguish campaigns that generate inexpensive traffic from those that generate more valuable downstream outcomes.

### 4.3 Cohort & Retention

Purpose: understand how acquired users behave after installation.

The retention workspace compares cohorts by acquisition month and channel using Day 1, Day 7, and Day 30 measures.

It supports questions such as:

- Which acquisition cohorts retain users more effectively?
- Does retention differ across channels?
- Are recent cohorts mature enough to evaluate at a particular milestone?
- Could strong acquisition metrics be hiding weak post-install behaviour?

Retention is evaluated with eligibility-aware denominators rather than treating every acquired user as immediately eligible for every milestone.

### 4.4 Experimentation Lab

Purpose: evaluate CRM treatment and control outcomes.

The experimentation workspace compares conversion rates across experiment groups and exposes the difference between observed lift and statistical evidence.

The analysis includes:

- Assigned users
- Conversion counts
- Conversion rates
- Absolute conversion lift
- Relative conversion lift
- Confidence intervals
- P-values and statistical significance
- Segment-level comparisons

The intention is to support disciplined experiment interpretation rather than relying only on a higher observed conversion rate.

### 4.5 Budget Simulator

Purpose: explore alternative budget allocations using historical performance as a reference.

The simulator lets users investigate what different spending scenarios could imply under the selected historical-rate assumptions.

It is a scenario-planning tool, not a promise that future campaign results will match historical performance.

A proper budget decision should also consider marginal returns, profitability, uncertainty, retention, and operational constraints.

---

## 5. Technology Stack

| Technology | Role in PulseGrowth |
|---|---|
| Python | Data generation, analytical scripts, validation, and application logic |
| Pandas | Data manipulation, aggregation, and preparation |
| SQL | Joins, filtering, grouping, KPI calculations, and transformations |
| DuckDB | Embedded analytical database |
| dbt Core | Reusable SQL models, data lineage, and transformation testing |
| dbt-duckdb | Connects dbt transformations to DuckDB |
| Streamlit | Interactive dashboard and application interface |
| Pytest | Automated testing of analytical behaviour |
| Statistical methods | Conversion comparisons, lift, confidence intervals, and significance testing |
| Git and GitHub | Version control and source management |
| Streamlit Community Cloud | Hosted dashboard deployment |

### Why this combination?

DuckDB supports analytical SQL without requiring a separate database server. dbt provides structure around transformations, while Python handles data generation and analytical logic.

Streamlit makes the results accessible through a web interface, and automated tests provide a way to detect regressions in important calculations.

The architecture is intentionally lightweight enough for a portfolio project while demonstrating patterns that are relevant to larger analytics systems.

---

## 6. System Architecture

PulseGrowth separates the data pipeline from the dashboard presentation layer.

```text
                 SYNTHETIC DATA GENERATION
                           |
                           v
                   SOURCE CSV DATASETS
                           |
                           v
                  DATA QUALITY VALIDATION
                           |
                           v
                    DUCKDB WAREHOUSE
                           |
                +----------+-----------+
                |                      |
                v                      v
          SQL / dbt MODELS       PYTHON ANALYTICS
                |                      |
                +----------+-----------+
                           |
                           v
                   ANALYTICAL DATA MARTS
                           |
                           v
                 CAMPAIGN DECISION TABLE
                           |
                           v
                  STREAMLIT DASHBOARD
                           |
                           v
                 BUSINESS INTERPRETATION
                           |
                           v
                MARKETING DECISION SUPPORT
```

### Layer 1 — Synthetic data generation

Python generates the source datasets using a fixed random seed, making the data generation reproducible when the same code and environment are used.

### Layer 2 — Data quality validation

The validation process checks expected structural and logical properties before downstream analysis.

This helps identify problems such as invalid records, missing expected fields, and violations of implemented data rules.

### Layer 3 — Analytical warehouse

DuckDB stores the source-oriented tables and supports SQL queries across advertising, acquisition, subscription, and experiment data.

### Layer 4 — Transformations

SQL and dbt transform source tables into staging models and analytical marts.

This layer is responsible for creating consistent analytical datasets from multiple sources.

### Layer 5 — Python analytics

Python scripts build the campaign decision table, perform attribution diagnostics, and support experiment analysis.

### Layer 6 — Presentation

Streamlit loads the analytical outputs and presents them through five interactive workspaces.

### Layer 7 — Decision support

The final layer translates metrics into investigation priorities and scenario comparisons. Business recommendations remain subject to interpretation and validation.

---

## 7. Data Generation and Dataset Design

The project uses synthetic data to model the relationships found in a subscription-oriented digital product.

The generator simulates advertising activity, user acquisition, product events, subscriptions, CRM experiments, and geographic experiment observations.

### 7.1 Dataset inventory

The recorded generation run produced the following datasets.

| Dataset | Rows | Purpose |
|---|---:|---|
| `campaigns.csv` | 16 | Campaign definitions and metadata |
| `ad_spend.csv` | 2,880 | Daily spend, impressions, and clicks |
| `users.csv` | 659,938 | User acquisition and attribution information |
| `app_events.csv` | 2,743,172 | Product activity events |
| `subscriptions.csv` | 58,404 | Subscription and revenue transactions |
| `crm_experiments.csv` | 395,963 | CRM experiment assignments and outcomes |
| `geo_experiments.csv` | 720 | Illustrative geographic experiment observations |

These figures describe the recorded generation run; they are not guaranteed to be identical if the generator changes.

### 7.2 Campaign design

The synthetic campaigns cover four acquisition channels:

- Google Ads
- Meta Ads
- TikTok Ads
- Apple Search Ads

The generated campaign set contains 16 campaigns across channel and campaign-theme combinations.

Daily advertising records simulate spend and engagement measurements, providing the basis for campaign-level aggregation.

### 7.3 User acquisition and attribution

The user dataset connects acquired users to acquisition information and campaign attribution.

The generator includes users whose acquisition channel is not identified. This is deliberate: it allows the platform to demonstrate attribution coverage and its effect on downstream reporting.

### 7.4 Product activity

The app-event dataset simulates user activity after acquisition.

These events support retention analysis by recording whether users return and generate activity after installation.

### 7.5 Subscription transactions

The subscription dataset provides transaction-level revenue information for the campaign and conversion analyses.

The attribution and aggregation logic determines how this revenue is associated with campaigns. It should not automatically be interpreted as incremental revenue.

### 7.6 CRM experiments

The CRM experiment dataset contains treatment/control assignments, segment information, and conversion outcomes.

The analysis uses this information to compare conversion rates and estimate uncertainty around the observed difference.

### 7.7 Geographic experiments

The geographic dataset provides illustrative market-level experiment observations.

It should be treated as a demonstration dataset unless a valid treatment design, comparison strategy, and causal estimation procedure have been independently established.

### 7.8 Reproducibility and date range

The recorded generation run used:

- **Random seed:** `42`
- **Start date:** 4 April 2026
- **End date:** 30 September 2026

A fixed random seed supports repeatable output for a given implementation. Changes to the generator or dependency environment can still affect results.

---

## 8. Data Quality and Validation

Data quality is a core part of the workflow because incorrect joins, missing identifiers, or inconsistent records can distort marketing KPIs.

The project includes a validation script:

```powershell
python src/ingestion/validate_data.py
```

The recorded validation run completed with **27 out of 27 checks passing**.

This means the datasets passed the implemented checks. It does not prove that every synthetic assumption reflects real-world marketing behaviour.

### Validation strategy

The validation stage is intended to catch issues before analytical models are built.

Relevant categories include:

1. **Structural validity:** Required files and expected fields exist.
2. **Data integrity:** Records follow the expected structure and data types.
3. **Logical consistency:** Values satisfy the implemented rules.
4. **Relationship checks:** Identifiers and relationships behave as expected.
5. **Analytical readiness:** Source data can be processed by the warehouse and downstream models.

The exact checks are defined in the validation implementation.

### Why validation matters

Suppose daily advertising spend is joined directly to multiple user events before aggregation. The same spend amount can be repeated across multiple joined rows, causing spend and revenue metrics to become inflated.

A reliable pipeline must therefore validate both the data and the grain at which the data is joined.

---

## 9. Data Warehouse and Data Model

The project uses DuckDB to store source-oriented tables and analytical marts.

### 9.1 Source-oriented warehouse tables

The full local warehouse contains tables including:

| Table | Purpose |
|---|---|
| `main.dim_campaigns` | Campaign metadata |
| `main.fct_ad_spend` | Advertising spend and engagement facts |
| `main.fct_users` | User acquisition and attribution records |
| `main.fct_app_events` | User activity events |
| `main.fct_subscriptions` | Subscription and revenue records |
| `main.fct_crm_experiments` | CRM experiment assignments and outcomes |
| `main.fct_geo_experiments` | Geographic experiment observations |

These tables support the broader analytical workflow and allow the source data to be examined directly.

### 9.2 Analytical marts

The warehouse also contains analytical outputs:

| Table | Purpose |
|---|---|
| `main.mart_campaign_performance` | Campaign-level performance measures |
| `main.mart_daily_campaign_performance` | Daily campaign trends |
| `main.mart_cohort_retention` | Cohort retention counts and rates |
| `analytics.mart_campaign_performance` | dbt campaign performance model consumed by the dashboard |
| `analytics.mart_crm_experiment_results` | Aggregated CRM experiment results consumed by the dashboard |

The `main` and `analytics` schemas contain distinct models. In particular, the two campaign performance marts should not be assumed to have identical columns or definitions.

### 9.3 Grain and aggregation strategy

The grain of a table describes what one row represents.

For example:

- An advertising fact may represent one campaign on one day.
- A user fact represents one user.
- An event fact represents an individual event.
- A subscription fact represents a subscription transaction.
- A daily campaign mart represents one campaign-day.
- A campaign performance mart represents one campaign.

Before joining datasets, their grains must be understood.

A robust aggregation strategy is to:

1. Aggregate spend to the required campaign or campaign-day grain.
2. Aggregate acquisition outcomes to the corresponding campaign grain.
3. Aggregate subscription revenue using the chosen attribution rule.
4. Join the aggregated results on appropriate keys.
5. Calculate ratios from the resulting counts and totals.

This reduces the risk of duplicated spend, inflated revenue, and inconsistent campaign KPIs.

### 9.4 Full warehouse versus deployment database

The full local warehouse contains the raw and transformed data required for development and rebuilding the analytics.

The deployed dashboard uses a smaller database, `data/processed/pulsegrowth_deploy.duckdb`, containing only the analytical tables required at runtime:

- `analytics.mart_campaign_performance`
- `analytics.mart_crm_experiment_results`
- `main.mart_cohort_retention`
- `main.mart_daily_campaign_performance`
- `main.fct_geo_experiments`

The compact database retains the required schema names and table structures while excluding the millions of raw event and user rows that the dashboard does not query directly.

This separation improves deployment practicality without replacing the full local warehouse used for analysis.

---

## 10. Marketing KPI Framework and Mathematical Logic

The KPI framework connects advertising activity to customer acquisition and attributed revenue.

Let:

- \(S\) = advertising spend
- \(I\) = impressions
- \(C\) = clicks
- \(A\) = attributed installs
- \(P\) = attributed paying customers
- \(R\) = revenue attributed to the campaign

The formulas below describe the analytical definitions used in the project. The implementation in the Python and SQL files remains the source of truth for the exact fields, aggregation rules, and edge-case handling.

### 10.1 Click-through rate (CTR)

CTR measures the proportion of impressions that generated clicks.

\[
\text{CTR}=\frac{C}{I}\times100
\]

**Example:** If a campaign receives 20,000 impressions and 500 clicks:

\[
\text{CTR}=\frac{500}{20,000}\times100=2.5\%
\]

**Interpretation:** CTR measures engagement with an advertisement. It does not establish whether the resulting users become valuable customers.

### 10.2 Cost per click (CPC)

CPC measures advertising cost per click.

\[
\text{CPC}=\frac{S}{C}
\]

**Example:** If spend is €1,000 and clicks total 500:

\[
\text{CPC}=\frac{1,000}{500}=€2
\]

A lower CPC can improve acquisition efficiency, but only if downstream conversion quality remains acceptable.

### 10.3 Cost per install (CPI)

CPI measures advertising spend per attributed install.

\[
\text{CPI}=\frac{S}{A}
\]

**Example:** If spend is €1,000 and the campaign generates 200 attributed installs:

\[
\text{CPI}=\frac{1,000}{200}=€5
\]

CPI is useful for evaluating install acquisition costs. It does not show how many acquired users become paying customers.

### 10.4 Customer acquisition cost (CAC)

The project uses an advertising-spend-based campaign CAC:

\[
\text{CAC}=\frac{S}{P}
\]

**Example:** If spend is €1,000 and 25 attributed customers pay:

\[
\text{CAC}=\frac{1,000}{25}=€40
\]

This is not necessarily fully loaded business CAC. A complete business CAC calculation may also include salaries, agency fees, creative production, incentives, and other acquisition expenses.

### 10.5 Install-to-payer conversion rate

This metric measures the proportion of attributed installs that become paying customers.

\[
\text{Install-to-payer rate}
=\frac{P}{A}\times100
\]

**Example:** If 25 of 200 attributed installs become paying customers:

\[
\text{Conversion rate}=\frac{25}{200}\times100=12.5\%
\]

This helps distinguish campaigns that generate inexpensive installs from those that generate paying customers.

### 10.6 Attributed revenue

Attributed revenue is the revenue assigned to a campaign under the project's attribution logic.

It connects revenue transactions to acquisition reporting but does not establish that the campaign caused the revenue.

The result depends on the attribution rules, revenue window, transaction definitions, and join logic.

### 10.7 Attributed return on advertising spend (ROAS)

ROAS compares attributed revenue with advertising spend.

\[
\text{ROAS}=\frac{R}{S}
\]

**Example:** If a campaign records €600 in attributed revenue from €1,000 in spend:

\[
\text{ROAS}=\frac{600}{1,000}=0.60\times
\]

This means the model attributes €0.60 of revenue to every €1 of advertising spend.

It does **not** mean the campaign generated €0.60 of profit per euro spent. Profitability depends on contribution margin, refunds, payment fees, retention, operating costs, and the period over which revenue is measured.

### 10.8 Aggregation and denominator safeguards

Ratios should be calculated from the appropriate underlying totals rather than by blindly averaging already-calculated percentages.

For example, the overall CTR should be:

\[
\text{Overall CTR}
=\frac{\sum_i C_i}{\sum_i I_i}\times100
\]

It should not generally be calculated as a simple average of campaign CTRs.

Similarly:

\[
\text{Overall CAC}
=\frac{\sum_i S_i}{\sum_i P_i}
\]

and:

\[
\text{Overall ROAS}
=\frac{\sum_i R_i}{\sum_i S_i}
\]

These formulas weight campaigns according to their underlying volumes.

If a denominator is zero, the implementation should use an explicitly defined null or fallback rather than presenting an invalid ratio as a meaningful result.

---

## 11. Campaign Performance and Decision Strategy

The Campaign Decision Centre turns the KPI framework into a structured campaign review process.

The objective is not simply to rank campaigns. It is to identify what should be investigated and why.

### 11.1 Multi-metric assessment

The decision table combines measures from different stages of the customer journey.

| Analytical dimension | Measures | Business question |
|---|---|---|
| Advertising engagement | CTR, CPC | Are impressions generating clicks efficiently? |
| Acquisition | Installs, CPI | What does it cost to acquire an install? |
| Conversion | Paying customers, CAC, install-to-payer rate | Are acquired users becoming paying customers? |
| Revenue efficiency | Attributed revenue, ROAS | How much attributed revenue is recorded relative to spend? |
| Data reliability | Attribution coverage | How complete is campaign attribution? |
| Retention | D1, D7, D30 retention | Do acquired users continue to engage? |

A campaign can perform well on one dimension and poorly on another. A low CPI, for example, does not guarantee a low CAC if few acquired users convert to paying customers.

### 11.2 Initial decision thresholds

The project's documented screening logic uses the following ROAS thresholds:

| Condition | Initial interpretation |
|---|---|
| Attributed ROAS at or above 1.0x | Promising enough for further evaluation |
| Attributed ROAS below 0.5x | Review campaign efficiency and economics |
| Between the thresholds | Monitor and examine supporting metrics |

These are project-specific screening thresholds, not universal marketing benchmarks.

A ROAS of 1.0x does not necessarily mean the campaign breaks even because revenue is not the same as contribution profit.

The thresholds are intended to prioritise investigation rather than automatically switch campaigns on or off.

### 11.3 Why the strategy uses multiple metrics

Consider two hypothetical campaigns:

- Campaign A generates many installs at a low CPI but has weak payer conversion.
- Campaign B generates fewer installs at a higher CPI but converts a larger share of users into paying customers.

Optimising solely for CPI may favour Campaign A even when Campaign B has a lower CAC or stronger attributed revenue efficiency.

A better decision workflow is:

1. Compare spend and engagement.
2. Evaluate install acquisition costs.
3. Examine payer conversion and CAC.
4. Compare attributed revenue and ROAS.
5. Check attribution completeness.
6. Review retention and experiment evidence where relevant.
7. Determine whether the result justifies further testing, monitoring, or budget review.

### 11.4 Decision outputs

The campaign decision table includes campaign identifiers and performance measures alongside a recommendation label.

The recommendation is a screening signal. It does not account for every business factor, such as contribution margin, lifetime value, market constraints, or diminishing returns.

A production implementation should make the threshold configuration explicit and test the recommendation boundaries.

---

## 12. Attribution Coverage and Reliability

Attribution coverage measures the proportion of users assigned to a recognised acquisition channel.

It is an important data-quality diagnostic because campaign performance comparisons depend on how completely users can be connected to acquisition sources.

### 12.1 Formula

\[
\text{Attribution coverage}
=\frac{\text{Attributed users}}{\text{Total users}}\times100
\]

The recorded synthetic run produced the following counts:

| Attribution category | Users |
|---|---:|
| Google Ads | 186,812 |
| Meta Ads | 165,574 |
| Apple Search Ads | 134,996 |
| TikTok Ads | 120,039 |
| Unattributed | 52,517 |
| **Total users** | **659,938** |

The number of attributed users was 607,421.

Therefore:

\[
\text{Coverage}
=\frac{607,421}{659,938}\times100
\approx92.04\%
\]

The remaining approximately 7.96% of users were unattributed in this generated output.

### 12.2 Why attribution coverage matters

Incomplete attribution can affect:

- Campaign-level CAC.
- Reported attributed revenue.
- Channel comparisons.
- Budget allocation decisions.
- The apparent distribution of acquisition sources.

Coverage is a completeness measure, not a measure of causal accuracy.

A dataset may have high attribution coverage and still assign users to channels incorrectly. A production analytics pipeline should therefore monitor both missing attribution and attribution validity.

---

## 13. Cohort Retention Analysis

Retention analysis measures whether users return after acquisition.

PulseGrowth groups users by acquisition month and channel, then evaluates activity at Day 1, Day 7, and Day 30.

### 13.1 Cohort definition

A cohort is a group of users sharing a defined acquisition period. In this project, users are grouped by acquisition month and channel.

The `main.mart_cohort_retention` model contains cohort information, eligible-user counts, retained-user counts, and retention rates.

### 13.2 Day 1 retention

\[
R_{D1}
=\frac{\text{Day 1 retained users}}
{\text{Day 1 eligible users}}\times100
\]

### 13.3 Day 7 retention

\[
R_{D7}
=\frac{\text{Day 7 retained users}}
{\text{Day 7 eligible users}}\times100
\]

### 13.4 Day 30 retention

\[
R_{D30}
=\frac{\text{Day 30 retained users}}
{\text{Day 30 eligible users}}\times100
\]

The denominator must include only users who have had enough observation time to reach the relevant milestone.

For example, someone who installed yesterday cannot yet be evaluated for Day 30 retention.

### 13.5 Weighted retention

When combining cohorts, overall retention should be calculated from total retained and eligible users:

\[
R_{\text{overall}}
=\frac{\sum_i \text{retained}_i}
{\sum_i \text{eligible}_i}\times100
\]

A simple average of cohort percentages can be misleading when cohort sizes differ substantially.

### 13.6 Business interpretation

Retention provides context that acquisition KPIs cannot supply on their own.

- High acquisition volume with weak retention may indicate low-quality acquisition.
- Strong retention with a high acquisition cost may justify evaluating longer-term customer value.
- Differences between channels may indicate differences in audience intent, product fit, or the generated data's underlying assumptions.

The dashboard also includes a retention-maturity diagnostic to highlight where observation windows need attention.

Because the synthetic data ends on 30 September 2026, recent cohorts require particular care when interpreting Day 30 results.

---

## 14. CRM Experimentation and Statistical Analysis

The CRM experimentation workflow compares conversion outcomes between treatment and control groups.

The central question is whether the observed conversion difference is large enough, relative to its uncertainty, to provide statistical evidence of an effect under the selected testing framework.

### 14.1 Conversion rate

For each experiment group:

\[
p=\frac{x}{n}
\]

where:

- \(x\) is the number of conversions.
- \(n\) is the number of assigned users.

The treatment and control conversion rates are denoted by \(p_T\) and \(p_C\).

### 14.2 Absolute conversion lift

\[
\Delta=p_T-p_C
\]

Absolute lift measures the difference between conversion rates. It is usually expressed in percentage points.

For example, an increase from 10% to 12% is an absolute lift of 2 percentage points.

### 14.3 Relative conversion lift

\[
\text{Relative lift}
=\frac{p_T-p_C}{p_C}\times100
\]

Relative lift expresses the difference in relation to the control rate.

It should be reported alongside absolute lift because a large relative increase can correspond to a small absolute change when the baseline conversion rate is low.

### 14.4 Hypothesis testing

The project uses a significance level of:

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

The null hypothesis states that there is no difference in the population conversion rates. The alternative states that a difference exists.

A p-value below 0.05 is classified as statistically significant under this framework.

A p-value is not the probability that the null hypothesis is true, nor does statistical significance automatically imply business value.

### 14.5 Confidence interval

A 95% confidence interval describes uncertainty around the estimated treatment-control difference under the selected method.

An interval that excludes zero is consistent with statistical significance for the corresponding two-sided test at the 5% level, provided the assumptions and method are appropriate.

### 14.6 Recorded synthetic results

The recorded synthetic experiment output reported:

| Metric | Control | Treatment |
|---|---:|---:|
| Assigned users | 198,038 | 197,925 |
| Conversions | 18,211 | 23,218 |
| Conversion rate | 9.20% | 11.73% |

The reported results were approximately:

- **Absolute lift:** +2.53 percentage points.
- **Relative lift:** +27.57%.
- **95% confidence interval:** approximately +2.34 to +2.73 percentage points.
- **P-value:** below the reported display precision of six decimal places.

These results demonstrate the workflow using generated data. They are not evidence that a real CRM campaign improved conversion.

### 14.7 Segment-level analysis

The project also examines outcomes across customer segments, including new, inactive, and trial users.

Segment-level comparisons can help generate hypotheses, but they also increase the risk of false-positive findings when many comparisons are performed.

A production experiment programme should define primary outcomes in advance and consider multiple-comparison adjustments when testing many segments.

### 14.8 Conditions for trustworthy experiments

Statistical calculations alone cannot guarantee a valid experiment.

A credible evaluation also depends on:

1. Correct treatment and control assignment.
2. Consistent outcome definitions.
3. Appropriate observation windows.
4. Independent or otherwise correctly modelled observations.
5. Adequate sample size.
6. Appropriate handling of missing outcomes and repeated users.
7. Consideration of multiple testing where relevant.

The quality of the experiment design is as important as the mathematical test.

---

## 15. Budget Simulator and Scenario Planning

The Budget Simulator explores how different allocations could translate into projected outcomes under historical performance assumptions.

The intention is to make the relationship between budget and expected outcomes transparent.

### 15.1 Scenario formulation

Let:

- \(B_i\) = proposed budget for campaign \(i\).
- \(r_i\) = selected historical performance ratio for campaign \(i\).
- \(\widehat{Y}_i\) = projected outcome for campaign \(i\).

A basic scenario formula is:

\[
\widehat{Y}_i=B_i\times r_i
\]

If the selected ratio is historical attributed ROAS:

\[
r_i=\frac{R_i}{S_i}
\]

then projected attributed revenue becomes:

\[
\widehat{R}_i
=B_i\times\frac{R_i}{S_i}
\]

### 15.2 Example

Suppose a campaign historically recorded €6,000 in attributed revenue from €10,000 in advertising spend.

Its historical attributed ROAS is:

\[
r=\frac{6,000}{10,000}=0.60
\]

Under a scenario that allocates €2,000 to the campaign:

\[
\widehat{R}=2,000\times0.60=€1,200
\]

This is a mechanical projection under a constant historical-rate assumption. It is not a prediction that the campaign will actually generate €1,200.

### 15.3 Strategic use

A budget simulator can help a marketing team:

- Compare alternative allocation scenarios.
- Understand the implications of moving spend between campaigns.
- Make historical performance assumptions explicit.
- Identify where additional experimentation or analysis is required.
- Discuss trade-offs between acquisition volume and attributed revenue efficiency.

### 15.4 Limitations of historical-rate scenarios

The formula assumes the selected historical performance ratio remains stable when spend changes.

In practice, additional spending can lead to:

- Audience saturation.
- Diminishing returns.
- Higher auction prices.
- Changes in traffic quality.
- Seasonal variation.
- Creative fatigue.
- Interactions between channels.
- Changes in customer conversion and retention.

A more advanced optimiser would model marginal returns, uncertainty, campaign-level constraints, and an explicit business objective.

For these reasons, PulseGrowth treats the simulator as an exploratory planning tool rather than a fully validated budget optimiser.

---

## 16. dbt Transformation Strategy

dbt is used to organise SQL transformations into named, reusable models.

The project includes staging models and analytical marts.

### 16.1 Staging models

Staging models organise and standardise source data before it is used in downstream analytics.

The project includes models such as:

- `stg_ad_spend`
- `stg_crm_experiments`
- `stg_subscriptions`
- `stg_users`

The staging layer provides a place to define consistent field names, types, and basic transformations.

### 16.2 Analytical marts

The project includes analytical models such as:

- `mart_campaign_performance`
- `mart_crm_experiment_results`

These models expose metrics and aggregates that can be consumed by the dashboard and other analytical workflows.

### 16.3 Why dbt?

The transformation framework supports:

- Reusable SQL logic.
- Declared data sources.
- Model-level testing.
- Repeatable transformation runs.
- More transparent data lineage.
- Easier maintenance of business logic.

### 16.4 Join-grain safeguards

Campaign performance combines data from advertising, user acquisition, subscriptions, and campaign metadata.

The sources have different grains, so they must be aggregated appropriately before joining.

Joining raw advertising records directly to multiple user events or subscription transactions can duplicate values and inflate results.

The transformation strategy therefore needs to make join keys, aggregation grain, attribution rules, and revenue definitions explicit.

### 16.5 Recorded dbt execution

The recorded full dbt run reported:

- 6 models.
- 17 tests.
- 7 sources.
- 6 out of 6 models completed successfully.
- 17 out of 17 tests passed.

These are results from the recorded development run, not a claim that every future run will produce the same output.

---

## 17. Testing and Analytical Quality Assurance

PulseGrowth uses automated checks at different stages of the analytical workflow.

### 17.1 Data validation

The synthetic-data validation script reported **27 out of 27 checks passing** in the recorded run.

### 17.2 dbt tests

The recorded dbt test run completed with **17 out of 17 tests passing**.

### 17.3 Pytest

The recorded project test run reported **15 tests passing**.

The test groups documented in the project include data-related behaviour, CRM experiment analysis, and campaign decision-table logic.

### 17.4 Why multiple testing layers?

Each layer tests a different part of the system.

| Layer | Purpose |
|---|---|
| Data validation | Check the generated source data |
| dbt tests | Check transformed models and declared rules |
| Python unit tests | Protect important analytical calculations |
| Dashboard validation | Confirm that the application loads and displays the required marts |

Passing tests do not guarantee that every business definition is correct. Analytical validation should also compare results against independently calculated values and verify the assumptions behind the metrics.

---

## 18. Deployment and Performance Strategy

The project separates the full development warehouse from the database required to serve the dashboard.

This was an important practical decision during deployment.

### 18.1 Why the full warehouse was not used directly

The full DuckDB warehouse reached approximately **105.26 MB** and contained millions of user and event rows.

The dashboard's data-loading code did not query all of these raw records directly. Instead, it consumed a small number of analytical marts.

Uploading and loading the full warehouse would therefore increase deployment size without providing a direct benefit to the current dashboard queries.

### 18.2 Compact deployment database

A separate database, `pulsegrowth_deploy.duckdb`, was created to retain the dashboard's required tables:

| Schema | Table | Recorded row count |
|---|---|---:|
| `analytics` | `mart_campaign_performance` | 16 |
| `analytics` | `mart_crm_experiment_results` | 8 |
| `main` | `mart_cohort_retention` | 30 |
| `main` | `mart_daily_campaign_performance` | 2,880 |
| `main` | `fct_geo_experiments` | 720 |

The five tables contain 3,654 rows in total.

The compact database was created from the full warehouse, preserving the schema and table names expected by the dashboard. The original full database remains useful for local development and pipeline rebuilding.

### 18.3 Deployment database selection

The Streamlit application is configured to load:

```python
DB_PATH = ROOT / "data" / "processed" / "pulsegrowth_deploy.duckdb"
```

The campaign decision table is stored separately:

```text
data/processed/campaign_decision_table.csv
```

Keeping these paths explicit makes the runtime dependency clear.

### 18.4 Version control strategy

The project excludes large generated datasets and local development artifacts from normal Git tracking. Only the compact deployment database and required decision table are deliberately included in the deployment commit.

This keeps the deployed application independent of the full raw data files while preserving the source code and the data needed to serve the current dashboard.

### 18.5 Deployment verification

After updating the application, the deployment should be checked for:

- Successful database loading.
- Correct schema and table availability.
- Successful rendering of all five workspaces.
- Correct loading of the campaign decision table.
- Absence of warehouse-not-found errors.
- Consistency between the deployed code and the latest GitHub commit.

The live application is available here:

**[Open PulseGrowth](https://pulsegrowth-marketing-intelligence-lrfpd5xacjdrrymdqzkqg9.streamlit.app/)**

---

## 19. End-to-End Setup Instructions

The instructions below describe how to set up the project locally using Windows PowerShell.

### Prerequisites

- Python 3.12.
- Git.
- PowerShell or another compatible shell.
- Internet access for dependency installation.

### Step 1 — Clone the repository

```powershell
git clone https://github.com/souravgupta166/Pulsegrowth-Marketing-Intelligence.git

cd Pulsegrowth-Marketing-Intelligence
```

### Step 2 — Create a virtual environment

```powershell
py -3.12 -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```powershell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### Step 4 — Generate the synthetic source data

```powershell
python src/ingestion/generate_data.py
```

This generates the source CSV datasets used by the pipeline.

### Step 5 — Validate the generated data

```powershell
python src/ingestion/validate_data.py
```

Review the output and resolve validation failures before proceeding.

### Step 6 — Build the DuckDB warehouse

```powershell
python src/analytics/build_warehouse.py
```

This builds the local analytical warehouse from the generated synthetic data.

### Step 7 — Run dbt transformations

From the repository root, use the project-specific paths:

```powershell
.\.venv\Scripts\dbt.exe run --project-dir dbt_project --profiles-dir dbt_project
```

### Step 8 — Run dbt tests

```powershell
.\.venv\Scripts\dbt.exe test --project-dir dbt_project --profiles-dir dbt_project
```

Review the output to confirm the models and tests completed successfully.

### Step 9 — Build the campaign decision table

```powershell
python src/analytics/build_campaign_decision_table.py
```

This creates the campaign-level decision output consumed by the application.

### Step 10 — Run the Python test suite

```powershell
python -m pytest -v
```

### Step 11 — Launch the dashboard

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL where the dashboard can be accessed.

### Reproducibility note

The full local pipeline generates the source data, builds the warehouse, runs dbt transformations, and produces the decision table.

The compact deployment database is a runtime artifact designed for the hosted dashboard. It should not be confused with the full warehouse used to rebuild and validate the analytical workflow.

---

## 20. Project Structure

The principal project files are organised as follows.

```text
Pulsegrowth-Marketing-Intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── synthetic/
│   └── processed/
│       ├── campaign_decision_table.csv
│       ├── pulsegrowth.duckdb
│       └── pulsegrowth_deploy.duckdb
│
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
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
│       ├── build_warehouse.py
│       ├── build_campaign_decision_table.py
│       ├── analyze_crm_experiment.py
│       └── attribution_coverage.py
│
├── tests/
│
└── docs/
```

This is a conceptual overview of the principal components. Individual files and subdirectories may evolve as the project develops.

The full warehouse and compact deployment database serve different purposes:

- `pulsegrowth.duckdb`: full local analytical warehouse.
- `pulsegrowth_deploy.duckdb`: compact database used by the deployed dashboard.
- `campaign_decision_table.csv`: campaign-level decision output.

---

## 21. Key Findings from the Synthetic Dataset

The recorded analytical run demonstrates several patterns worth investigating in a marketing analytics workflow.

### 21.1 Attribution completeness

The generated dataset reported approximately **92.04% attribution coverage**, with 52,517 users remaining unattributed.

This demonstrates why attribution coverage should be examined before relying on channel-level comparisons.

### 21.2 Campaign efficiency differences

In the recorded campaign decision output, Apple Search Ads campaigns had higher attributed ROAS than the other represented channels.

The synthetic results are useful for demonstrating campaign comparisons, but they should not be treated as evidence that Apple Search Ads is inherently more effective in real marketing environments.

### 21.3 CRM conversion lift

The generated treatment group recorded a higher seven-day conversion rate than the control group:

- Control: 9.20%.
- Treatment: 11.73%.
- Reported absolute lift: approximately +2.53 percentage points.

The experiment analysis demonstrates how conversion differences, confidence intervals, and significance can be evaluated. The result is generated, not a real campaign outcome.

### 21.4 Retention and cohort maturity

The retention workflow demonstrates why Day 1, Day 7, and Day 30 metrics must use eligible-user denominators.

Recent acquisition cohorts need sufficient observation time before their retention outcomes can be compared fairly with older cohorts.

### 21.5 The broader analytical lesson

Acquisition, attribution, revenue, retention, and experimentation answer different questions.

- Acquisition metrics describe cost and volume.
- Attribution connects recorded outcomes to campaigns.
- Retention describes subsequent user behaviour.
- Experiments evaluate treatment-control differences under a defined design.
- Budget scenarios explore implications under explicit assumptions.

A sound marketing decision considers these signals together rather than treating a single KPI as sufficient.

---

## 22. Business Recommendations and Decision Framework

The analytical framework suggests a structured way to turn marketing data into action.

### Recommendation 1 — Avoid optimising only for installs

Use CPI as an acquisition-efficiency measure, but evaluate it alongside payer conversion and CAC.

**Reason:** Cheap installs do not necessarily become paying customers.

### Recommendation 2 — Treat ROAS as an investigation signal

Use attributed ROAS to compare campaigns, but consider revenue timing, contribution margins, refunds, retention, and attribution assumptions before deciding whether a campaign is profitable.

**Reason:** Attributed revenue is not the same as incremental profit.

### Recommendation 3 — Include retention in channel evaluation

Compare Day 1, Day 7, and Day 30 retention alongside acquisition costs.

**Reason:** A campaign that acquires users efficiently but loses them quickly may have weaker long-term economics than its initial metrics suggest.

### Recommendation 4 — Use experiments for causal questions

When the question is whether a CRM intervention improves conversion, use a well-designed treatment-control experiment rather than relying exclusively on campaign attribution.

**Reason:** Descriptive associations and causal effects are different types of evidence.

### Recommendation 5 — Use budget scenarios cautiously

Explore alternative allocations using historical performance, then validate important assumptions with additional data or experiments.

**Reason:** Historical performance may not remain constant as spend changes.

### Recommendation 6 — Make data quality visible

Track attribution completeness, denominator eligibility, model tests, and source-to-mart consistency.

**Reason:** An apparently strong KPI is only as reliable as the data and definitions behind it.

### Recommended decision sequence

```text
1. Validate data quality
          |
          v
2. Check attribution completeness
          |
          v
3. Compare acquisition and conversion
          |
          v
4. Review attributed revenue and ROAS
          |
          v
5. Examine retention and experiment evidence
          |
          v
6. Explore budget scenarios
          |
          v
7. Make a decision with explicit assumptions
          |
          v
8. Monitor the next observed outcome
```

This sequence is a decision framework, not an automatic optimisation algorithm.

---

## 23. Limitations and Responsible Interpretation

PulseGrowth is an educational portfolio project. Its outputs need to be interpreted within the limits of its data and modelling assumptions.

### Synthetic data

The generated datasets do not represent real users, advertising accounts, customers, or company performance.

The results demonstrate the analytical workflow, not verified commercial outcomes.

### Attribution is not causality

Campaign attribution assigns recorded outcomes according to a selected rule. It does not prove that advertising generated incremental revenue.

### Historical performance is not a guaranteed forecast

Campaign performance can change as spending, audiences, creative assets, competition, and market conditions change.

### CAC is narrowly defined

The project-level CAC calculation uses advertising spend divided by attributed paying customers. It does not necessarily include all costs required for a fully loaded acquisition measure.

### Retention requires appropriate observation windows

Users must have enough elapsed time to become eligible for Day 1, Day 7, or Day 30 retention measurements.

### Statistical significance is not business significance

A statistically significant difference may be too small to matter commercially. A non-significant result does not automatically establish that the treatment has no effect.

### Experiment quality depends on design

Valid interpretation depends on assignment, outcome definitions, observation windows, assumptions, and the selected statistical method.

### Geographic experiment data are illustrative

The presence of geographic observations does not, by itself, establish a valid causal experiment.

### Budget scenarios depend on assumptions

Historical-rate scenarios do not model every real-world constraint, such as diminishing returns, audience saturation, or changes in marginal acquisition costs.

### Deployment and reproducibility

The compact database is intended to serve the current dashboard. The full analytical workflow remains the source for rebuilding the warehouse and validating transformations.

---

## 24. Future Roadmap

PulseGrowth provides a foundation for further analytical and engineering improvements.

### 24.1 Incrementality measurement

Implement and validate a user-level or geographic causal analysis with an explicit treatment design, comparison strategy, and estimation method.

### 24.2 Customer lifetime value

Estimate customer lifetime value using subscription history and clearly documented assumptions about retention, revenue, and costs.

### 24.3 Advanced budget optimisation

Develop marginal response curves, diminishing-return assumptions, campaign-level constraints, and an explicit optimisation objective.

### 24.4 Attribution diagnostics

Add more detailed checks for missing identifiers, conflicting assignments, and differences between attributed and unattributed populations.

### 24.5 Retention maturity

Validate retention eligibility at the individual-user level and add boundary-date tests for each retention milestone.

### 24.6 Metric governance

Standardise KPI definitions across Python scripts, SQL models, dbt transformations, and dashboard outputs.

### 24.7 Stronger data contracts

Introduce more explicit schema, uniqueness, referential-integrity, and source-to-mart reconciliation tests.

### 24.8 Experiment quality

Add sample-size planning, predefined primary outcomes, and appropriate multiple-comparison handling for segment analysis.

### 24.9 Monitoring

Track data-volume changes, pipeline failures, missing values, and unexpected KPI shifts.

### 24.10 Decision traceability

Record which metrics, assumptions, thresholds, and constraints contributed to each campaign recommendation or budget scenario.

These improvements would move the project towards a more robust marketing decision-support system.

---

## 25. Skills Demonstrated

PulseGrowth demonstrates an integrated set of business analytics, data engineering, statistical analysis, and application development skills.

| Area | Skills demonstrated |
|---|---|
| Business analysis | KPI definition, campaign evaluation, decision frameworks, strategic interpretation |
| SQL | Joins, aggregations, data modelling, analytical transformations |
| Python | Data generation, data processing, validation, analytical scripts |
| DuckDB | Analytical warehouse design and querying |
| dbt | Staging models, marts, reusable SQL, transformation tests |
| Marketing analytics | CTR, CPC, CPI, CAC, conversion rates, attributed ROAS |
| Product analytics | Cohort analysis, retention, user activity |
| Experimentation | Treatment-control comparisons, conversion lift, confidence intervals, hypothesis testing |
| Data quality | Validation rules, denominator checks, aggregation-grain awareness |
| Dashboard development | Streamlit application, analytical visualisation, decision-oriented presentation |
| Testing | Pytest, dbt tests, validation workflows |
| Deployment | Git, GitHub, compact deployment artifacts, Streamlit Community Cloud |

The central learning from this project is that useful analytics requires more than calculating metrics. It requires defining the business question, validating the underlying data, choosing the right denominator, understanding uncertainty, and communicating what the result does—and does not—justify.

---

## 26. Author

**Sourav Gupta**

GitHub: [github.com/souravgupta166](https://github.com/souravgupta166)

LinkedIn: [linkedin.com/in/sourav-gupta-7539a9217](https://www.linkedin.com/in/sourav-gupta-7539a9217/)

### Project links

- **Live dashboard:** [PulseGrowth — Marketing Intelligence](https://pulsegrowth-marketing-intelligence-lrfpd5xacjdrrymdqzkqg9.streamlit.app/)
- **Source code:** [GitHub repository](https://github.com/souravgupta166/Pulsegrowth-Marketing-Intelligence)

---

*PulseGrowth is an educational portfolio project. All reported business results are generated from synthetic data and should not be interpreted as real commercial outcomes.*
