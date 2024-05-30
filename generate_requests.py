import requests
import time

for i in range(3):
    params = {
        'x': str(i),
        'y': '2',
    }
    response = requests.get('http://localhost:1702/predict', params=params)
    time.sleep(10)