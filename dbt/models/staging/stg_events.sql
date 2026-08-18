select
    event_id::bigint as event_id,
    user_id::bigint as user_id,
    event_ts::timestamp as event_ts,
    event_ts::date as event_date,
    lower(event_name) as event_name
from {{ source('rewardiq', 'events') }}
