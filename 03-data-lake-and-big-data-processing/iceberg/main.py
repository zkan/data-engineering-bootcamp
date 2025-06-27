import datetime
import os

import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.expressions import And, EqualTo, GreaterThan, In, IsNull, StartsWith
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.schema import Schema
from pyiceberg.transforms import DayTransform
from pyiceberg.types import IntegerType, FloatType, NestedField, StringType, TimestampType


# กำหนด Home Directory สำหรับ PyIceberg
os.environ["PYICEBERG_HOME"] = os.getcwd()

# โหลด Catalog ที่ชื่อ local ที่เรากำหนดในไฟล์ .pyiceberg.yaml มา
catalog = load_catalog(name="local")
print(catalog.properties)

# สร้าง Namespace หรือ Database ที่ชื่อ transactions
catalog.create_namespace_if_not_exists("transactions")

# กำหนด Partition ของข้อมูลโดยใช้ฟิลด์ created_at (เลข ID ที่ 4)
partition_spec = PartitionSpec(
    PartitionField(
        source_id=4, field_id=1000, transform=DayTransform(), name="created_at_day"
    )
)
# กำหนด Schema (หรือ Table)
schema = Schema(
    NestedField(field_id=1, name="id", field_type=IntegerType(), required=True),
    NestedField(field_id=2, name="category", field_type=StringType(), required=True),
    NestedField(field_id=3, name="amount", field_type=FloatType(), required=True),
    NestedField(field_id=4, name="created_at", field_type=TimestampType(), required=True),
    NestedField(field_id=5, name="updated_at", field_type=TimestampType(), required=False),
    # Mark id as the identifier field, also known as the primary-key
    identifier_field_ids=[1],
)
# สร้าง Iceberg Table จาก Schema และ Partition ที่กำหนด
iceberg_table = catalog.create_table_if_not_exists(
    identifier="transactions.sales_data",
    schema=schema,
    partition_spec=partition_spec,
)
print(iceberg_table.schema())

# Create a PyArrow table with some sample transactions
pa_table_data = pa.Table.from_pylist(
    [
        {"id": 1, "category": "electronics", "amount": 299.99, "created_at": datetime.datetime(2025, 5, 1)},
        {"id": 2, "category": "clothing", "amount": 79.99, "created_at": datetime.datetime(2025, 5, 30)},
        {"id": 3, "category": "groceries", "amount": 45.50, "created_at": datetime.datetime(2025, 5, 30)},
        {"id": 4, "category": "electronics", "amount": 999.99, "created_at": datetime.datetime(2025, 6, 2)},
        {"id": 5, "category": "clothing", "amount": 120.00, "created_at": datetime.datetime(2025, 6, 2)},
    ],
    schema=iceberg_table.schema().as_arrow(),
)

## Appending
# iceberg_table.append(df=pa_table_data)

## Upserting
iceberg_table.upsert(df=pa_table_data)

print(iceberg_table.scan().to_arrow().to_string(preview_cols=10))

# Querying Iceberg tables

## Query rows where the "category" column starts with "elec"
result = iceberg_table \
    .scan(row_filter=StartsWith("category", "elec")) \
    .to_arrow()
print(result.to_string(preview_cols=3))

# print(iceberg_table.inspect.partitions())
# print(iceberg_table.inspect.history())

## Get timestamp for 7 days ago
seven_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
## Query rows where 'created_at' is greater than seven days ago
result = iceberg_table \
    .scan(row_filter=GreaterThan("created_at", seven_days_ago)) \
    .to_arrow()
print(result.to_string(preview_cols=3))

## Query rows where "category" is "clothing" and "amount" is greater than 80
result = iceberg_table \
    .scan(
        row_filter=And(
            EqualTo("category", "clothing"),
            GreaterThan("amount", 80)
        )
    ) \
    .to_arrow()
print(result.to_string(preview_cols=10))

## Retrieve only "category" and "amount" for records where "id" = 3
result = iceberg_table \
    .scan(
        row_filter=EqualTo("id", 3),
        selected_fields=["category", "amount"]
    ) \
    .to_arrow()
print(result.to_string(preview_cols=10))

## Find rows where "amount" is NULL
result = iceberg_table \
    .scan(row_filter=IsNull("amount")) \
    .to_arrow()
print(result.to_string(preview_cols=10))

## Query rows where "category" is in ["clothing", "groceries"]
result = iceberg_table \
    .scan(row_filter=In("category", ["clothing", "groceries"])) \
    .to_arrow()
print(result.to_string(preview_cols=10))

# Updating and Deleting Data

## Updating
filtered_table = iceberg_table \
  .scan(row_filter=EqualTo("id", 4)) \
  .to_arrow()
print(filtered_table.to_string(preview_cols=5))

updated_at_col_index = filtered_table.column_names.index("updated_at")
print(updated_at_col_index)
updated_at_col_field = filtered_table.field(updated_at_col_index)
print(updated_at_col_field)

now = datetime.datetime.now()
## Replace the "updated_at" column with the new timestamp value
updated_table = filtered_table.set_column(
  updated_at_col_index, 
  updated_at_col_field, 
  pa.array([now])
)
## Overwrite the existing row in the Iceberg table
iceberg_table.overwrite(
  df=updated_table,
  overwrite_filter=EqualTo("id", 4)
)

result = iceberg_table \
    .scan() \
    .to_arrow()
print(result.to_string(preview_cols=10))

## Deleting
iceberg_table.delete(
    delete_filter=EqualTo("id", 1)
)

result = iceberg_table \
    .scan() \
    .to_arrow()
print(result.to_string(preview_cols=10))

# Schema Evolution in Iceberg
with iceberg_table.update_schema() as update:
    update.add_column("email", StringType())

print(catalog.load_table("transactions.sales_data").schema())

with iceberg_table.update_schema() as update:
    update.delete_column("email")

print(catalog.load_table("transactions.sales_data").schema())
