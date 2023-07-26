with

source as (

    select * from {{ source('greenery', 'products') }}

)

, renamed_recasted as (

    select
        product_id as product_guid
        , name as product_name
        , price
        , inventory

    from source

)

select * from renamed_recasted