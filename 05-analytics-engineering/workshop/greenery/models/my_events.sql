{{
    config(
        materialized="table",
        partition_by={
            "field": "created_at",
            "data_type": "timestamp",
            "granularity": "day"
        }
    )
}}

select * from {{ source('greenery', 'events') }}
