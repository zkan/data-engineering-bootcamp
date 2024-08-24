import json

import avro.schema
import pandas as pd
import pyarrow.orc as orc
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


print("### CSV ###")
df_csv = pd.read_csv("homes.csv")
df_csv.columns = [
    "Sell",
    "List",
    "Living",
    "Rooms",
    "Beds",
    "Baths",
    "Age",
    "Acres",
    "Taxes",
]
print(df_csv.head())

print("### JSON ###")
df_csv.to_json("homes.json")
df_json = pd.read_json("homes.json")
print(df_json.head())

# Ref: http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html
with open("widgets.json") as data_file:    
    data = json.load(data_file)
    
df_widgets_json = pd.json_normalize(data)
print(df_widgets_json.head())

print("### Parquet ###")
df_csv.to_parquet("homes.parquet")
df_pq = pd.read_parquet("homes.parquet")
print(df_pq.head())

## CLI: parquet-tools inspect --detail homes.parquet

print("### Avro ###")
schema_file_name = "user.avsc"
output_file_name = "users.avro"
schema = avro.schema.parse(open(schema_file_name, "rb").read())
print(schema)

writer = DataFileWriter(open(output_file_name, "wb"), DatumWriter(), schema)
writer.append({"name": "Alyssa", "favorite_number": 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.close()

reader = DataFileReader(open(output_file_name, "rb"), DatumReader())
# Get schema from Avro file
print(reader.datum_reader.writers_schema)
print(reader.meta.get('avro.schema').decode('utf-8'))

for user in reader:
    print(user)

reader.close()

print("### ORC ###")
df_csv.to_orc("homes.orc")
df_orc = pd.read_orc("homes.orc")
print(df_orc.head())

data_reader = orc.ORCFile("homes.orc")
data = data_reader.read()
print(data)
print(data.to_pydict())

print("### XML ###")
df_xml = pd.read_xml("coordinates.xml")
print(df_xml.head())

df_xml.to_xml("coordinates_new.xml", index=None)
