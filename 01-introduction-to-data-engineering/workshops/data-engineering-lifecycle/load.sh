#!/bin/bash

curl -XPOST -H "Content-type: application/json" -d @dogs.json "https://getpantry.cloud/apiv1/pantry/bc53e13f-cc03-4ed0-a5bc-24651a8f8aa4/basket/random_dogs"