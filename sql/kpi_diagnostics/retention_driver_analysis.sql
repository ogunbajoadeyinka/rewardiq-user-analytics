-- Diagnose D30 retention movement across acquisition channel and platform.
-- Uses a 28-32 day window to make retention less sensitive to a single exact day.
with eligible_users as (
    select
        u.user_id,
        u.signup_date,
        date_trunc('month', u.signup_date)::date as signup_month,
        u.acquisition_channel,
        u.platform,
        u.activated_7d,
        max(case
            when e.event_ts::date between u.signup_date + 28 and u.signup_date + 32
            then 1 else 0
        end) as retained_d30
    from rewardiq.users u
    left join rewardiq.events e
      on e.user_id = u.user_id
     and e.event_name = 'app_open'
    where u.signup_date <= date '2025-11-29'
    group by 1,2,3,4,5,6
),
segment_metrics as (
    select
        signup_month,
        acquisition_channel,
        platform,
        activated_7d,
        count(*) as users,
        sum(retained_d30) as retained_users,
        avg(retained_d30::numeric) as d30_retention
    from eligible_users
    group by 1,2,3,4
),
with_previous as (
    select *,
        lag(d30_retention) over (
            partition by acquisition_channel, platform, activated_7d
            order by signup_month
        ) as previous_month_retention
    from segment_metrics
)
select
    signup_month,
    acquisition_channel,
    platform,
    activated_7d,
    users,
    retained_users,
    round(d30_retention, 4) as d30_retention,
    round(previous_month_retention, 4) as previous_month_retention,
    round(d30_retention - previous_month_retention, 4) as mom_change_pp
from with_previous
order by signup_month, mom_change_pp asc nulls last;
