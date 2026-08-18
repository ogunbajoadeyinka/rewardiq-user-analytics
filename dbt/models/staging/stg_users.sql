select
    user_id::bigint as user_id,
    signup_date::date as signup_date,
    lower(acquisition_channel) as acquisition_channel,
    lower(platform) as platform,
    lower(region) as region,
    activated_7d::boolean as activated_7d
from {{ source('rewardiq', 'users') }}
