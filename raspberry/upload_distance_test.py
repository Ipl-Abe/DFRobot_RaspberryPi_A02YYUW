import hashlib
import hmac
import requests
import datetime
import json
import os
import time
import numpy as np



path = os.path.expanduser('~/.API_KEYS/machinist_keys.json')
#path = os.path.abspath("~/.API_KEYS/machinist_keys.json")

f = open(path)

json_data = json.load(f)
data = json_data['keys']
#print(data['API_KEY'])


url = ""


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ${json_data['keys']}",
}
data = '{"agent": "Home", "metrics":{"name": "temperature", "namespace": "Environment Sensor", "data_point": {"value": 27.6}}}'
response = requests.post('https://gw.machinist.iij.jp/endpoint', headers=headers, data=data)
print(response.text)


