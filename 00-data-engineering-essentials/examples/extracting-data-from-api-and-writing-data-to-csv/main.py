import csv

import requests


# Read data from API
url = "https://api.coincap.io/v2/exchanges"
response = requests.get(url)
data = response.json()["data"]

# Write data to CSV
with open("exchanges.csv", "w") as f:
    fieldnames = [
        "exchangeId",
        "name",
        "rank",
        "percentTotalVolume",
        "volumeUsd",
        "tradingPairs",
        "socket",
        "exchangeUrl",
        "updated",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for each in data:
        writer.writerow(each)
