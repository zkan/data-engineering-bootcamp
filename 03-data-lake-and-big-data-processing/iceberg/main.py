import os

import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, IntegerType, StringType, FloatType


os.environ['PYICEBERG_HOME'] = os.getcwd()

catalog = load_catalog(name='local')
print(catalog.properties)

catalog.create_namespace_if_not_exists('transactions')
schema = Schema(
    NestedField(field_id=1, name="id", field_type=IntegerType(), required=True),
    NestedField(field_id=2, name="category", field_type=StringType(), required=True),
    NestedField(field_id=3, name="amount", field_type=FloatType(), required=True),
    # Mark id as the identifier field, also known as the primary-key
    identifier_field_ids=[1],
)
iceberg_table = catalog.create_table_if_not_exists(
    identifier="transactions.sales_data",
    schema=schema
)
print(iceberg_table.schema())

# Create a PyArrow table with some sample transactions
pa_table_data = pa.Table.from_pylist(
    [
        {"id": 1, "category": "electronics", "amount": 299.99},
        {"id": 2, "category": "clothing", "amount": 79.99},
        {"id": 3, "category": "groceries", "amount": 45.50},
        {"id": 4, "category": "electronics", "amount": 999.99},
        {"id": 5, "category": "clothing", "amount": 120.00},
    ],
    schema=iceberg_table.schema().as_arrow(),
)
# iceberg_table.append(df=pa_table_data)
iceberg_table.upsert(df=pa_table_data)
print(iceberg_table.scan().to_arrow().to_string(preview_cols=10))

# Querying Iceberg tables
from pyiceberg.expressions import StartsWith

# Query rows where the "category" column starts with "elec"
result = iceberg_table \
    .scan(row_filter=StartsWith("category", "elec")) \
    .to_arrow()
print(result.to_string(preview_cols=3))

# from pyiceberg.expressions import GreaterThan
# import datetime
# # Get timestamp for 7 days ago
# seven_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
# # Query rows where 'created_at' is greater than seven days ago
# result = iceberg_table \
#     .scan(row_filter=GreaterThan('created_at', seven_days_ago)) \
#     .to_arrow()
# print(result.to_string(preview_cols=10))

# from pyiceberg.expressions import And, EqualTo, GreaterThan
# # Query rows where 'category' is "A" and 'value' is greater than 20
# result = iceberg_table \
#     .scan(
#         row_filter=And(
#             EqualTo('category', 'A'),
#             GreaterThan('value', 20)
#         )
#     ) \
#     .to_arrow()
# print(result.to_string(preview_cols=10))

# from pyiceberg.expressions import EqualTo
# # Retrieve only 'id' and 'value' for records where 'id' = 3
# result = iceberg_table \
#     .scan(
#         row_filter=EqualTo('id', 3),
#         selected_fields=['id', 'value']
#     ) \
#     .to_arrow()
# print(result.to_string(preview_cols=10))

# from pyiceberg.expressions import IsNull
# # Find rows where 'value' is NULL
# result = iceberg_table \
#     .scan(row_filter=IsNull('value')) \
#     .to_arrow()
# print(result.to_string(preview_cols=10))

# from pyiceberg.expressions import In
# # Query rows where 'id' is in [2, 4, 6]
# result = iceberg_table \
#     .scan(row_filter=In('id', [2, 4, 6])) \
#     .to_arrow()
# print(result.to_string(preview_cols=10))

