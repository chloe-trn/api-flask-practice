# send a request for testing 
import requests

# location of API
BASE = "http://127.0.0.1:5000/"

# wanna send a GET request to the URL of base+"helloworld"
# {} is data sent with the request , this is called a FORM

data = [
    {"likes": 2, "name": "Joes", "views": 1000},
    {"likes": 200, "name": "DIY", "views": 140},
    {"likes": 550, "name": "HOW to", "views": 1330},
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + 'video/5')
print(response.json())
input()
response = requests.delete(BASE + 'video/0')
print(response)
