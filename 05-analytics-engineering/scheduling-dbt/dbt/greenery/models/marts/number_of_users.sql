with

users as (

		select * from {{ ref('stg_greenery__users') }}

)

, final as (

		select 
				count(distinct user_guid) as number_user

		from users

)

select * from final