with

orders as (

    select * from {{ ref('stg_greenery__orders') }}

)

, orders_cohort as (

    select
        user_guid
        , count(distinct order_guid) as user_orders

    from orders
    group by 1

)

, users_bucket as (

    select
        user_guid
        , cast(user_orders >= 2 as integer) as has_two_purchases

    from orders_cohort

)

, final as (

    select
        cast(sum(has_two_purchases) as float64) / cast(count(distinct user_guid) as float64) as repeat_rate
		
    from users_bucket

)

select * from final