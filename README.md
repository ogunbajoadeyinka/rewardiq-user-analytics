# RewardIQ — User Analytics & Experimentation Platform

An end-to-end product analytics portfolio project focused on user acquisition, activation, engagement, conversion, retention, segmentation, and experimentation.

## Business Problem

RewardIQ is a fictional consumer rewards platform. User acquisition is growing, but 30-day retention has declined. This project investigates what is driving the decline, which users are affected, and which product or lifecycle interventions should be tested.

## Questions This Project Answers

- Where do users drop off between signup, activation, first transaction, reward redemption, and repeat engagement?
- How do D1, D7, D14, and D30 retention vary by acquisition channel and cohort?
- Which behavioral and lifecycle segments have the highest value and churn risk?
- What explains changes in core KPIs?
- Are proposed product interventions statistically likely to improve user outcomes?
- Should an experiment launch, iterate, or stop?

## Analytics Stack

- **SQL / PostgreSQL** — data modeling, funnels, cohorts, retention, segmentation, KPI analysis
- **dbt Core** — transformation, testing, documentation, reusable analytics marts
- **Python** — experimentation, power analysis, MDE, statistical testing, automation
- **Hex** — SQL/Python exploratory analysis and experiment readouts
- **Tableau Public** — interactive portfolio dashboard
- **Git/GitHub** — version control and project documentation

## Planned Analytics Layers

1. Raw users, app events, transactions, rewards, campaigns, and experiments
2. dbt staging models and source validation
3. Intermediate user-event and transaction models
4. Analytics marts for funnels, cohorts, retention, segments, and experiments
5. Statistical experimentation workflow
6. Executive and self-service dashboards

## Dashboard Views

1. Executive User Health
2. Acquisition & Activation Funnel
3. Retention & Cohort Analysis
4. User Segmentation
5. Experimentation Center
6. KPI Diagnostic / “What Changed?”

## Experimentation

The experimentation module will demonstrate:

- Hypothesis and metric definition
- Minimum Detectable Effect (MDE)
- Statistical power and sample-size estimation
- Control vs. treatment analysis
- Confidence intervals and statistical significance
- Segment-level treatment effects
- Launch / Iterate / Stop recommendations

## Data Strategy

The project will use a hybrid dataset: legitimate public retail/e-commerce data where appropriate, supplemented with clearly documented simulated mobile-app events, lifecycle attributes, and experiment assignments. Synthetic fields will never be presented as proprietary company data.

## Repository Structure

```text
rewardiq-user-analytics/
├── data/
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── tests/
├── sql/
│   ├── funnels/
│   ├── retention/
│   ├── segmentation/
│   └── kpi_diagnostics/
├── python/
│   └── experimentation/
├── dashboard/
├── docs/
└── README.md
```

## Status

🚧 In development — data architecture and analytics modeling are the first implementation phase.

---

**Portfolio focus:** Product Analytics · User Analytics · Growth Analytics · Experimentation · SQL · dbt · Python · Tableau