# RewardIQ Metric Definitions

This document defines the initial source-of-truth metrics used throughout the project.

## Acquisition

**New Users** — distinct users whose signup timestamp falls within the reporting period.

## Activation

**Activated User** — a signed-up user who completes a first qualifying transaction within 7 days of signup.

**Activation Rate** — activated users / new users in the eligible signup cohort.

## Engagement

**DAU** — distinct users with at least one qualifying app engagement event on a calendar day.

**WAU** — distinct users with at least one qualifying engagement event during the trailing 7-day window.

**MAU** — distinct users with at least one qualifying engagement event during the trailing 30-day window.

**DAU/MAU** — DAU divided by MAU; used as a stickiness indicator.

## Conversion

**Transaction Conversion Rate** — users completing a qualifying transaction / eligible users entering the measured funnel.

**Reward Redemption Rate** — users redeeming a reward / users earning or becoming eligible for a reward.

## Retention

**D1 Retention** — share of a signup cohort returning for qualifying activity one day after signup.

**D7 Retention** — share returning seven days after signup.

**D14 Retention** — share returning fourteen days after signup.

**D30 Retention** — share returning thirty days after signup.

Retention definitions will use explicit activity windows in the SQL models to prevent inconsistent interpretation.

## Lifecycle Segments

Initial segments:

- New
- Activated
- Highly Engaged
- High Value
- At Risk
- Dormant
- Resurrected
- Power User

Segment rules will be implemented centrally in the analytics layer rather than duplicated in dashboards.

## Experimentation

**Primary Metric** — outcome selected before experiment analysis to determine the main treatment effect.

**MDE** — minimum detectable effect the experiment is designed to reliably detect at the selected power and significance level.

**Lift** — relative or absolute difference between treatment and control, explicitly labeled in experiment outputs.

**Decision** — Launch, Iterate, or Stop based on statistical evidence, practical significance, guardrail metrics, and business context.
