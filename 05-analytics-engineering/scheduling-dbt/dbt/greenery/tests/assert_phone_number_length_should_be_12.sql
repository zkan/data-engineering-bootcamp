select
    length(phone_number)

from {{ ref('my_users') }}
where length(phone_number) != 12