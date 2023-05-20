import json

import requests


if __name__ == "__main__":
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = response.json()

    # Your code here
    print(data)

    with open("dogs.json", "w") as f:
        json.dump(data, f)