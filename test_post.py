# test_post.py — Send signal to webhook without CLI madness

import requests
import json

url = "http://localhost:5000/webhook"

payload = {
    "pair": "EURUSD",
    "message": "💹 TradingView BUY SIGNAL — Test Success"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.status_code, response.text)
