import requests
import json

payload = {
    "input": "Привет. Как дела?"
}

response = requests.post(url='http://0.0.0.0:8000/invoke', data=json.dumps(payload))
print(response.json())