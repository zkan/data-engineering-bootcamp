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

mydict = { "Cusomter_id": "A85123", "Country": "UK" }
x = mycol.insert_one(mydict)
print(x.inserted_id) 

mylist = []
mylist.append({ "Cusomter_id": "B85123", "Country": "DE" })
mylist.append({ "Cusomter_id": "C85123", "Country": "US" })
x = mycol.insert_many(mylist)
print(x.inserted_ids) 
