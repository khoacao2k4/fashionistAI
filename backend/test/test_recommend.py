import requests

# API URL
url = "http://127.0.0.1:5000/recommend_old"  # Update if the server runs on a different host/port

# Test payload
payload = {
    "clothes": [
        {
            "id": 1234,
            "subCategory": "Accessories",
            "articleType": "Watches",
            "gender": "Men",
            "baseColour": "Blue",
            "season": "Summer",
            "usage": "Sports"
        },
        {
            "id": 5678,
            "subCategory": "T-Shirts",
            "articleType": "Casual",
            "gender": "Men",
            "baseColour": "White",
            "season": "Winter",
            "usage": "Formal"
        },
        {
            "id": 9876,
            "subCategory": "Jackets",
            "articleType": "Outerwear",
            "gender": "Unisex",
            "baseColour": "Black",
            "season": "Winter",
            "usage": "Casual"
        }
    ],
    "occasion": "party",
    "n": 2
}

# Headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request
response = requests.post(url, json=payload, headers=headers)

# Print response
if response.status_code == 200:
    print("Recommendations:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.json())