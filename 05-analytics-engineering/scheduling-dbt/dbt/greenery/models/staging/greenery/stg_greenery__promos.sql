with source as (

    select * from {{ source('greenery', 'promos') }}

),

renamed_recasted as (

    select
        promo_id as promo_guid
        , cast(discount as string) as discount
        , status as promo_status
    from source

)

select * from renamed_recasted