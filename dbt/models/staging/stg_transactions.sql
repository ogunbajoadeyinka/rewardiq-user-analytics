select
    transaction_id::bigint as transaction_id,
    user_id::bigint as user_id,
    transaction_ts::timestamp as transaction_ts,
    transaction_ts::date as transaction_date,
    amount::numeric(12,2) as amount,
    lower(status) as status
from {{ source('rewardiq', 'transactions') }}
