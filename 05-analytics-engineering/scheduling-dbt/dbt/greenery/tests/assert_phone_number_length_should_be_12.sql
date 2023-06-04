select
    length(phone_number)

from {{ ref('users') }}
where length(phone_number) != 12