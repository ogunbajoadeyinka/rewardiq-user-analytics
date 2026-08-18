-- D1 / D7 / D14 / D30 exact-day retention by signup cohort and acquisition dimensions.
WITH activity AS (
    SELECT DISTINCT
        u.user_id,
        DATE_TRUNC('month', u.signup_date)::date AS signup_cohort,
        u.acquisition_channel,
        u.platform,
        (e.event_ts::date - u.signup_date) AS days_since_signup
    FROM rewardiq.users u
    JOIN rewardiq.events e ON e.user_id = u.user_id
    WHERE e.event_name = 'app_open'
),
cohort_size AS (
    SELECT
        DATE_TRUNC('month', signup_date)::date AS signup_cohort,
        acquisition_channel,
        platform,
        COUNT(*) AS users
    FROM rewardiq.users
    GROUP BY 1,2,3
)
SELECT
    c.signup_cohort,
    c.acquisition_channel,
    c.platform,
    c.users AS cohort_users,
    ROUND(COUNT(DISTINCT CASE WHEN a.days_since_signup = 1 THEN a.user_id END)::numeric / c.users, 4) AS d1_retention,
    ROUND(COUNT(DISTINCT CASE WHEN a.days_since_signup = 7 THEN a.user_id END)::numeric / c.users, 4) AS d7_retention,
    ROUND(COUNT(DISTINCT CASE WHEN a.days_since_signup = 14 THEN a.user_id END)::numeric / c.users, 4) AS d14_retention,
    ROUND(COUNT(DISTINCT CASE WHEN a.days_since_signup = 30 THEN a.user_id END)::numeric / c.users, 4) AS d30_retention
FROM cohort_size c
LEFT JOIN activity a
  ON a.signup_cohort = c.signup_cohort
 AND a.acquisition_channel = c.acquisition_channel
 AND a.platform = c.platform
GROUP BY 1,2,3,4
ORDER BY 1,2,3;
