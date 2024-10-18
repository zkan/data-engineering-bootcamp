with

int_orders_products__joined as (

    select * from {{ ref('int_orders_products__joined') }}

)

, final as (

    select
        order_guid
        , order_created_at_utc
        , order_cost_usd
        , shipping_cost_usd
        , order_total_usd
        , shipping_service
        , estimated_delivery_at_utc
        , delivered_at_utc
        , order_status
        , user_guid
        , promo_guid
        , user_created_at_utc
        , zipcode
        , state
        , country
        , quantity
        , product_name
        , price
        , inventory

    from int_orders_products__joined

)

select * from final