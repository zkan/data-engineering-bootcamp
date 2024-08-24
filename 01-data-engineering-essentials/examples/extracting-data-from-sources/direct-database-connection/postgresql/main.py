import csv
import configparser
import datetime

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("postgres_config", "database")
user = parser.get("postgres_config", "username")
password = parser.get("postgres_config", "password")
host = parser.get("postgres_config", "host")
port = parser.get("postgres_config", "port")

conn_str = f"dbname={dbname} user={user} password={password} host={host} port={port}"
conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

print("### Extraction by Specific Date ###")
tables = [
    ("events", datetime.date(2021, 2, 10)),
    ("orders", datetime.date(2021, 2, 10)),
    ("users", datetime.date(2020, 5, 4)),
]
for table, dt in tables:
    query = f"select * from {table} where date(created_at) = '{dt}' limit 3"
    print(query)
    cursor.execute(query)

    results = cursor.fetchall()
    for each in results:
        print(each)

    print("-" * 5)

print("### Full Extraction ###")
"""
When table has no primary key and date, we can calculate the difference between
source and the destination

with destination as (
    select 'c615ea16-2b87-471c-a40e-f1a1b81df308' as order_id, 'e18f33a6-b89a-4fbc-82ad-ccba5bb261cc' as product_id, 2 as quantity
)

select * from order_items where product_id = 'e18f33a6-b89a-4fbc-82ad-ccba5bb261cc'
except
select * from destination order by quantity;
"""
tables = [
    "addresses",
    "order_items",
    "products",
    "promos",
]
for table in tables:
    query = f"select * from {table} limit 3"
    print(query)
    cursor.execute(query)

    results = cursor.fetchall()
    for each in results:
        print(each)

    print("-" * 5)


print("#### Full Extraction using Pandas ###")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")
df = pd.read_sql("select * from orders", engine)
print(df.head(3))

print("### Incremental Extraction ###")
"""
The last_extraction_run is a timestamp representing the most recent run of the
extraction job. The value can be retrieved from the following SQL executed in a
data warehouse:

select max(last_updated) from warehouse.orders
"""
dt = datetime.datetime(2021, 2, 11, 14, 23, 40, 656219)
last_extraction_run = dt
query = f"select * from orders where created_at > '{last_extraction_run}' limit 3"
print(query)
cursor.execute(query)

results = cursor.fetchall()
for each in results:
    print(each)

print("-" * 5)

cursor.close()
conn.close()
