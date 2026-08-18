select
    date_trunc('month', signup_date)::date as signup_month,
    acquisition_channel,
    platform,
    count(*) as signed_up_users,
    count(*) filter (where first_app_open_at is not null) as app_opened_users,
    count(*) filter (where receipt_scan_count > 0) as receipt_scanners,
    count(*) filter (where first_transaction_at is not null) as transacting_users,
    count(*) filter (where transaction_activated_7d) as activated_7d_users,
    round(count(*) filter (where transaction_activated_7d)::numeric / nullif(count(*), 0), 4) as activation_rate_7d
from {{ ref('int_user_activity') }}
group by 1,2,3
