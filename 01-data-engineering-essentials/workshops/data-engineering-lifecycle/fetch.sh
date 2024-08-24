#!/bin/bash

API_KEY='YOUR_API_KEY'
COLLECTION_ID='YOUR_COLLECTION_ID'

curl -XGET \
    -H "X-Master-key: $API_KEY" \
    "https://api.jsonbin.io/v3/c/$COLLECTION_ID/bins"
