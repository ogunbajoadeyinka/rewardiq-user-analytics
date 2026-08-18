# RewardIQ Dashboard Specification

## 1. Executive User Health

**Purpose:** Give Product, Growth, and Marketing leaders a fast view of user health.

KPI cards: New Users, Activation Rate, Transaction Conversion, D7 Retention, D30 Retention, Gross Transaction Value.

Visuals: monthly KPI trend, acquisition-channel mix, platform split, retention trend. Filters: date, acquisition channel, platform, region.

## 2. Acquisition & Activation Funnel

Funnel: Signup → App Open → Receipt Scan → First Transaction → Activated in 7 Days.

Show stage conversion, stage-to-stage drop-off, acquisition channel, platform, and monthly cohort comparisons.

## 3. Retention & Cohorts

Cohort heatmap plus D1/D7/D14/D30 trend lines. Enable channel/platform drill-down. Highlight statistically and commercially meaningful deterioration rather than only displaying averages.

## 4. User Segmentation

Show lifecycle segment size, transaction value, engagement, activation, and retention. Include New, Activated, Highly Engaged, High Value, At Risk, Dormant, Low Engagement, and Power User segments.

## 5. Experimentation Center

Experiment selector, hypothesis, primary metric, control/treatment sizes, conversion rates, absolute/relative lift, p-value, confidence interval, MDE, power, guardrails, and a Launch / Iterate / Stop recommendation.

## 6. KPI Diagnostic — What Changed?

Start with D30 retention movement, then decompose by acquisition channel → platform → activation status → cohort. Rank segments by contribution to KPI deterioration so stakeholders can move from symptom to likely driver.

## UX Principles

- Executive summary first; detail on demand.
- Consistent metric definitions sourced from dbt marts.
- Tooltips contain metric definitions and business interpretation.
- Filters persist across relevant views.
- Avoid decorative visuals that do not support a decision.
- Every analytical page ends with a short “So what?” insight or recommended action.
