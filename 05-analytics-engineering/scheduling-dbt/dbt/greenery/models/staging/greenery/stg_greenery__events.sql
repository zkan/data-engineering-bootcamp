with source as (

    select * from {{ source('greenery', 'events') }}

),

renamed_recasted as (

    select
        event_id as event_guid
        , session_id as session_guid
        , page_url
        , created_at as created_at_utc
        , event_type
        , user as user_guid
        , `order` as order_guid
        , product as prodcut_guid
    from source
)

select * from renamed_recasted