with

events as (

    select * from {{ ref('stg_greenery__events') }}

)

, unique_sessions as (

    select
        count(distinct session_guid) as number_of_unique_sessions
        
    from events

)

, unique_add_to_cart_sessions as (

    select
        count(distinct session_guid) as number_of_unique_add_to_cart_sessions
        
    from events
    where event_type = 'add_to_cart'

)

, final as (

    select
        number_of_unique_add_to_cart_sessions
        , number_of_unique_sessions
        , cast(number_of_unique_add_to_cart_sessions as float64) / cast(number_of_unique_sessions as float64) as add_to_cart_rate
		
    from
        unique_add_to_cart_sessions
        , unique_sessions

)

select * from final