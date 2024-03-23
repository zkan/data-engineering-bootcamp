select
    user_id
    , length(phone_number) as phone_number_length

from {{ ref('my_users') }}
where length(phone_number) != 12