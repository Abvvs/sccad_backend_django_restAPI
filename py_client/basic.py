import requests

#endpoint = "http://localhost/status/200"
#endpoint = "http://127.0.0.1:8000/"
endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.get(endpoint, json= {'query':'hello world'}) #HTTP REQUEST
#print(get_response.json()['message'])
#print(get_response.text)
#print(get_response.status_code)
print(get_response.json())