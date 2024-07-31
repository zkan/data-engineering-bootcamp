{{ config(materialized='table') }}
select * from {{ source('greenery', 'users') }}
where email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' = true