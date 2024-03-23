{{
    config(
        materialized='view'
    )
}}

select * from {{ source('greenery', 'users') }}