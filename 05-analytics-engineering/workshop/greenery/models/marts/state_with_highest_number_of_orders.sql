with

orders as (

		select * from {{ ref('stg_greenery__orders') }}

)

, addresses as (

    select * from {{ ref('stg_greenery__addresses') }}

)

, final as (

    select
        state
        , count(o.order_guid) as number_of_orders

    from orders as o
    join addresses as a
        on o.address_guid = a.address_guid
    group by state
    order by 2 desc
    limit 1

)

select * from final