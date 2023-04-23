import requests


API_URL = "http://34.87.139.82:8000/"
DATA = "events"
DATE = "2021-02-10"

response = requests.get(f"{API_URL}/{DATA}/?created_at={DATE}")
data = response.json()
for each in data:
    print(each["event_id"], each["event_type"])