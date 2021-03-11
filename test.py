# send a request for testing 
import requests

# location of API
BASE = "http://127.0.0.1:5000/"

# wanna send a GET request to the URL of base+"helloworld"
# {} is data sent with the request , this is called a FORM

# use get request to get what you just sent 
response = requests.get(BASE + 'video/6')
print(response)