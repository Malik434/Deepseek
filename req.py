import requests

url = "http://127.0.0.1:5000/analyze"
data = {"text": "I hate waiting in long lines. Its so frustrating!"}

response = requests.post(url, json=data)
print(response.json()) 