with source as (

    select * from {{ source('greenery', 'orders') }}

),

renamed_recasted as (

    select
        order_id as order_guid
        , user as user_guid
        , promo as promo_guid
        , address as address_guid
        , created_at as order_created_at_utc
        , order_cost as order_cost_usd
        , shipping_cost as shipping_cost_usd
        , order_total as order_total_usd
        , tracking_id as tracking_guid
        , shipping_service
        , estimated_delivery_at as estimated_delivery_at_utc
        , delivered_at as delivered_at_utc
        , status as order_status

    from source

)

select * from renamed_recasted