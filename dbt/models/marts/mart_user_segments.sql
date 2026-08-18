with base as (
    select *,
        (date '2026-01-15' - last_app_open_at::date) as days_since_last_activity
    from {{ ref('int_user_activity') }}
)
select
    *,
    case
        when signup_date >= date '2026-01-15' - 14 then 'New'
        when completed_transactions >= 8 and active_days >= 15 then 'Power User'
        when gross_transaction_value >= 500 then 'High Value'
        when active_days >= 12 then 'Highly Engaged'
        when days_since_last_activity between 15 and 30 then 'At Risk'
        when days_since_last_activity > 30 then 'Dormant'
        when transaction_activated_7d then 'Activated'
        else 'Low Engagement'
    end as lifecycle_segment
from base
