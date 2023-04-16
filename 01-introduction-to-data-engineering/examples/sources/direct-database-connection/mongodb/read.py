import configparser

import pymongo


parser = configparser.ConfigParser()
parser.read("pipeline.conf")
username = parser.get("mongo_config", "username")
password = parser.get("mongo_config", "password")
host = parser.get("mongo_config", "host")
port = parser.get("mongo_config", "port")

# Connect to mongodb
myclient = pymongo.MongoClient(f"mongodb://{host}:{port}/", username=username, password=password)
mydb = myclient["test"]  # select the database
mycol = mydb["testcol"]  # select the collection

myquery = {}
mydoc = mycol.find(myquery).sort("Cusomter_id", 1)
for x in mydoc:
    print(x)

# how to sort the data that you will retrieve
# find order ASC .sort("Cusomter_id") or .sort("Cusomter_id", 1)
# find order DSC .sort("Cusomter_id",-1)  
print("-" * 10)

myquery = {"Cusomter_id": "A85123"}
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)

print("-" * 10)

myreturnonly = {"_id": 0, "Cusomter_id": 1}
mydoc = mycol.find(myquery, myreturnonly)
for x in mydoc:
    print(x)

print("-" * 10)
