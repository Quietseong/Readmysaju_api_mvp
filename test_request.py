import requests
import json

url = "http://127.0.0.1:8000/chat"
headers = {"Content-Type": "application/json"}
data = {
    "message": "1990년 3월 15일 오전 9시에 태어난 여자입니다. 운세가 궁금해요"
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2)) 