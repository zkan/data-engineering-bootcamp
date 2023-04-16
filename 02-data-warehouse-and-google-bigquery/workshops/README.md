# Data Warehouse and Google BigQuery Workshop

## Arrays, Structs, and JSON

### Arrays

```sql
with a as (
    select ["current", "previous", "birth"] as address_history
)

select address_history from a
```

### Unnesting an Array

```sql
with a as (
    select ["current", "previous", "birth"] as address_history
)

select addr
from
  a
  , unnest(address_history) as addr
```

### Structs

```sql
with a as (
    select
   	    struct(
            "current" as status,
            "London" as address,
            "ABC123D" as postcode
   	    ) as address_history
)

select address_history from a
```

### Array of Structs

```sql
with a as (
	select [
        struct("current" as status,"London" as address, "ABC123D" as postcode)
        , struct("previous" as status,"New Delhi" as address, "738497" as postcode)
        , struct("birth" as status,"New York" as address, "SHI747H" as postcode)
	] as address_history
)

select address_history from a
```

### Unnesting Array of Structs

```sql
with a as (
	select [
        struct("current" as status,"London" as address, "ABC123D" as postcode)
        , struct("previous" as status,"New Delhi" as address, "738497" as postcode)
        , struct("birth" as status,"New York" as address, "SHI747H" as postcode)
	] as address_history
)

select addr from a, unnest(address_history) as addr
```

### Working with JSON

```sql
select
    json_query('{ "name" : "Jakob", "age" : "6" }', '$.name') as json_name
    , json_value('{ "name" : "Jakob", "age" : "6" }', '$.name') as scalar_name
    , json_query('{ "name" : "Jakob", "age" : "6" }', '$.age') as json_age
    , json_value('{ "name" : "Jakob", "age" : "6" }', '$.age') as scalar_age
```

```sql
select
    json_query('{"fruits": ["apple", "banana"]}', '$.fruits') as json_query
    , json_value('{"fruits": ["apple", "banana"]}', '$.fruits') as json_value
```