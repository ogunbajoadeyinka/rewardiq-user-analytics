with assignments as (
    select
        user_id,
        experiment_id,
        variant,
        assigned_at::timestamp as assigned_at
    from {{ source('rewardiq', 'experiment_assignments') }}
),
post_assignment_activity as (
    select
        a.user_id,
        a.experiment_id,
        a.variant,
        a.assigned_at,
        max(case
            when e.event_name = 'app_open'
             and e.event_ts > a.assigned_at
             and e.event_ts <= a.assigned_at + interval '7 day'
            then 1 else 0 end) as retained_7d,
        count(distinct e.event_date) filter (
            where e.event_ts > a.assigned_at
              and e.event_ts <= a.assigned_at + interval '7 day'
        ) as active_days_7d
    from assignments a
    left join {{ ref('stg_events') }} e on e.user_id = a.user_id
    group by 1,2,3,4
),
post_assignment_txns as (
    select
        a.user_id,
        count(t.transaction_id) filter (
            where t.transaction_ts > a.assigned_at
              and t.transaction_ts <= a.assigned_at + interval '7 day'
              and t.status = 'completed'
        ) as transactions_7d,
        coalesce(sum(t.amount) filter (
            where t.transaction_ts > a.assigned_at
              and t.transaction_ts <= a.assigned_at + interval '7 day'
              and t.status = 'completed'
        ), 0) as gtv_7d
    from assignments a
    left join {{ ref('stg_transactions') }} t on t.user_id = a.user_id
    group by 1
)
select
    p.*,
    coalesce(t.transactions_7d, 0) as transactions_7d,
    coalesce(t.gtv_7d, 0) as gtv_7d
from post_assignment_activity p
left join post_assignment_txns t using (user_id)
