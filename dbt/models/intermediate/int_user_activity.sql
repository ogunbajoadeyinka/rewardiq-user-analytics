with users as (
    select * from {{ ref('stg_users') }}
),
events as (
    select
        user_id,
        min(event_ts) filter (where event_name = 'app_open') as first_app_open_at,
        max(event_ts) filter (where event_name = 'app_open') as last_app_open_at,
        count(*) filter (where event_name = 'app_open') as app_open_count,
        count(*) filter (where event_name = 'receipt_scan') as receipt_scan_count,
        count(distinct event_date) as active_days
    from {{ ref('stg_events') }}
    group by 1
),
transactions as (
    select
        user_id,
        min(transaction_ts) as first_transaction_at,
        count(*) filter (where status = 'completed') as completed_transactions,
        sum(amount) filter (where status = 'completed') as gross_transaction_value
    from {{ ref('stg_transactions') }}
    group by 1
)
select
    u.*,
    e.first_app_open_at,
    e.last_app_open_at,
    coalesce(e.app_open_count, 0) as app_open_count,
    coalesce(e.receipt_scan_count, 0) as receipt_scan_count,
    coalesce(e.active_days, 0) as active_days,
    t.first_transaction_at,
    coalesce(t.completed_transactions, 0) as completed_transactions,
    coalesce(t.gross_transaction_value, 0) as gross_transaction_value,
    case when t.first_transaction_at::date <= u.signup_date + 7 then true else false end as transaction_activated_7d
from users u
left join events e using (user_id)
left join transactions t using (user_id)
