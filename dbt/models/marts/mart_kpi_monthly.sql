with users as (
    select * from {{ ref('int_user_activity') }}
),
retention as (
    select * from {{ ref('mart_user_retention') }}
),
monthly_users as (
    select
        date_trunc('month', signup_date)::date as month,
        acquisition_channel,
        platform,
        count(*) as new_users,
        count(*) filter (where transaction_activated_7d) as activated_users,
        count(*) filter (where completed_transactions > 0) as transacting_users,
        sum(completed_transactions) as completed_transactions,
        sum(gross_transaction_value) as gross_transaction_value
    from users
    group by 1,2,3
),
monthly_retention as (
    select
        signup_month as month,
        acquisition_channel,
        platform,
        avg(retained_d1::numeric) as d1_retention,
        avg(retained_d7::numeric) as d7_retention,
        avg(retained_d14::numeric) as d14_retention,
        avg(retained_d30::numeric) as d30_retention
    from retention
    group by 1,2,3
)
select
    u.month,
    u.acquisition_channel,
    u.platform,
    u.new_users,
    u.activated_users,
    round(u.activated_users::numeric / nullif(u.new_users, 0), 4) as activation_rate,
    u.transacting_users,
    round(u.transacting_users::numeric / nullif(u.new_users, 0), 4) as transaction_conversion_rate,
    u.completed_transactions,
    round(u.gross_transaction_value, 2) as gross_transaction_value,
    round(r.d1_retention, 4) as d1_retention,
    round(r.d7_retention, 4) as d7_retention,
    round(r.d14_retention, 4) as d14_retention,
    round(r.d30_retention, 4) as d30_retention
from monthly_users u
left join monthly_retention r using (month, acquisition_channel, platform)
