import csv
import configparser
import datetime

import psycopg2


parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("postgres_config", "database")
user = parser.get("postgres_config", "username")
password = parser.get("postgres_config", "password")
host = parser.get("postgres_config", "host")
port = parser.get("postgres_config", "port")

conn_str = f"dbname={dbname} user={user} password={password} host={host} port={port}"
conn = psycopg2.connect(conn_str)

today = datetime.date(2021, 2, 11)

tables = [
    "events",
    "orders",
    "users",
]
for table in tables:
    query = f"SELECT * FROM {table} WHERE date(created_at) = '{today}'"
    cursor = conn.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    for each in results:
        print(each)

    print("-" * 15)


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
    query = f"SELECT * FROM {table}"
    cursor = conn.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    for each in results:
        print(each)

    print("-" * 15)
