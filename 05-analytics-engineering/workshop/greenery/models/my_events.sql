-- config your document
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

-- query code that you want to save
select * from {{ source('greenery', 'events') }}