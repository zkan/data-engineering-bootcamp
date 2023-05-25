with

source as (

    select * from {{ source('greenery', 'order_items') }}

)

, renamed_recasted as (

    select
        order_id as order_guid
        , product_id as product_guid
        , quantity

    from source

)

select * from renamed_recasted