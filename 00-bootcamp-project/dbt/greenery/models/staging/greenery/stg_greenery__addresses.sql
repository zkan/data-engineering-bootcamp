with source as (

    select * from {{ source('greenery', 'addresses') }}

),

renamed_recasted as (

    select
        address_id as address_guid
        , address
        , cast(zipcode as string) as zipcode
        , state
        , country

    from source

)

select * from renamed_recasted