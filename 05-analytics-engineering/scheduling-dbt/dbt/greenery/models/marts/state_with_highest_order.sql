with
orders as (
		select * from {{ ref('stg_greenery__orders') }}
)

, state_from_orders as (
        select
				ord.order_guid,
                ord.address_guid,  
                adr.state
		from orders ord
        left join {{ ref('stg_greenery__addresses') }} adr on 
            ord.address_guid = adr.address_guid
)
, state_from_orders_distinct as (
		select
				distinct *
		from state_from_orders
)
, final as (
    select
        state
        , count(order_guid) as number_of_order
    from state_from_orders_distinct
    group by state
    order by number_of_order desc 
    limit 1
)

select * from final 