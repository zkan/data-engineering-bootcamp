import json

import subprocess

import requests


if __name__ == "__main__":
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = response.json()

    print(data)

    test = {
        "สวัสดี" : "ODDS"
    }

    with open("dogs.json", "a") as files : 
        json.dump(data, files)

    subprocess.run("./load.sh")    
    # Your code here