{% snapshot users_snapshot %}

{{
    config(
      target_database='greenery',
      target_schema='snapshots',
      unique_key='user_id',

      strategy='timestamp',
      updated_at='updated_at',
    )
}}

select * from {{ source('greenery', 'users') }}

{% endsnapshot %}
