#!/bin/bash

curl -XPOST -H "Content-type: application/json" -d @dogs.json "https://getpantry.cloud/apiv1/pantry/<YOUR-PANTRY-ID>/basket/randomDogs"