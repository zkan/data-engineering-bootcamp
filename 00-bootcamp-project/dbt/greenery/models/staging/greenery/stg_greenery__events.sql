with

source as (

    select * from {{ source('greenery', 'events') }}

)

, renamed_recasted as (

    select
        event_id as event_guid
        , session_id as session_guid
        , user_id as user_guid
        , page_url
        , created_at as event_created_at_utc
        , event_type
        , order_id as order_guid
        , product_id as product_guid

    from source

)

select * from renamed_recasted
