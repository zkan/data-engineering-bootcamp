with

orders as (

		select * from {{ ref('stg_greenery__orders') }}

)

, final as (

		select
				count(distinct order_guid) as number_of_order

		from orders

)

select * from final