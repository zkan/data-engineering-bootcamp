select
    *
from {{ source('greenery', 'events') }}