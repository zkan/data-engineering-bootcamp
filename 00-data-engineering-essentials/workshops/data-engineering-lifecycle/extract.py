import json

import requests


if __name__ == "__main__":
    url = ""
    response = requests.get(url)
    data = response.json()

    # Your code here