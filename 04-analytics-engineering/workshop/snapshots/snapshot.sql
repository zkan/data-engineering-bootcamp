{% snapshot booking_snapshot %}

{{
  config(
	target_schema='snapshots',
	unique_key='booking_no',
	strategy='timestamp',
	updated_at='update_date',
  )
}}

select * from {{ source('main', 'booking') }}

{% endsnapshot %}
