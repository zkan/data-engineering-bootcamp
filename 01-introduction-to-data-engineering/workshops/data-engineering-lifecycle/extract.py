import json

import requests


if __name__ == "__main__":
    url = "https://dog.ceo/api/breeds/image/random" #add any API url your want to get data
    #requests.get = to get data
    #requests.post= to send data
    response = requests.get(url) 
    data = response.json()


    # Your code here
    print(data)
    with open("dogs.json","w") as f:
        json.dump(data,f)