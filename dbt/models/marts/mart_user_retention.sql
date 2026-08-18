with users as (
    select * from {{ ref('stg_users') }}
),
activity as (
    select distinct user_id, event_date
    from {{ ref('stg_events') }}
    where event_name = 'app_open'
),
retention as (
    select
        u.user_id,
        u.signup_date,
        date_trunc('month', u.signup_date)::date as signup_month,
        u.acquisition_channel,
        u.platform,
        u.region,
        u.activated_7d,
        max(case when a.event_date = u.signup_date + 1 then 1 else 0 end) as retained_d1,
        max(case when a.event_date between u.signup_date + 6 and u.signup_date + 8 then 1 else 0 end) as retained_d7,
        max(case when a.event_date between u.signup_date + 13 and u.signup_date + 15 then 1 else 0 end) as retained_d14,
        max(case when a.event_date between u.signup_date + 28 and u.signup_date + 32 then 1 else 0 end) as retained_d30
    from users u
    left join activity a on a.user_id = u.user_id
    group by 1,2,3,4,5,6,7
)
select * from retention
