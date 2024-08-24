with source as (

    select * from {{ ref('my_hello_world') }}

)

, final as (

    select
        greeting

    from source

)

select * from final