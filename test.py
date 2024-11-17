import requests
import json

# Base URL for the Flask API
BASE_URL = "http://127.0.0.1:5000"

# Test image file paths
TEST_IMAGES = ["test/1.jpg", "test/2.jpg"]

def test_predict(image_path):
    """
    Test the /predict API for a single image.
    """
    url = f"{BASE_URL}/predict"
    with open(image_path, "rb") as img_file:
        files = {"file": img_file}
        response = requests.post(url, files=files)
        print(f"Testing /predict with {image_path}...")
        print(f"Status Code: {response.status_code}")
        return response.json() if response.status_code == 200 else None

def test_get_all():
    """
    Test the /get_all API.
    """
    url = f"{BASE_URL}/get_all"
    response = requests.get(url)
    print(f"Testing /get_all...")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=4)}")
    return response.json() if response.status_code == 200 else None

def test_update_metadata(record_id):
    """
    Test the /update_metadata API for a single record.
    """
    url = f"{BASE_URL}/update_metadata"
    payload = {
        "id": record_id,
        "subCategory": "Updated Category",
        "article": "Updated Article",
        "gender": "Updated Gender",
        "color": "Updated Color",
        "season": "Updated Season",
        "usage": "Updated Usage"
    }
    response = requests.put(url, json=payload)
    print(f"Testing /update_metadata for record_id: {record_id}...")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_delete_image(record_id):
    """
    Test the /delete_image API for a single record.
    """
    url = f"{BASE_URL}/delete_image"
    payload = {"id": record_id}
    response = requests.delete(url, json=payload)
    print(f"Testing /delete_image for record_id: {record_id}...")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def recommend_clothes(clothes, occasion, n=5):
    """
    Test the /recommend API for a single set of clothes and an occasion.
    """
    url = f"{BASE_URL}/recommend"
    payload = {"clothes": clothes, "occasion": occasion, "n": n}
    response = requests.post(url, json=payload)
    print(f"Testing /recommend for clothes: {clothes} and occasion: {occasion}...")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Starting API Tests...\n")

    # 1. Test /predict for multiple images
    print("Step 1: Testing /predict for multiple images...")
    for image_path in TEST_IMAGES:
        test_predict(image_path)
    print("Step 1 Completed.\n")

    # 2. Test /get_all to retrieve all records
    print("Step 2: Testing /get_all to fetch all records...")
    all_records = test_get_all()
    if not all_records or len(all_records) == 0:
        print("No records found. Exiting tests.")
        exit(1)
    print("Step 2 Completed.\n")

    # 3. Test /update_metadata for the first record
    print("Step 3: Testing /update_metadata for the first record...")
    first_record_id = all_records[0].get("id")
    if first_record_id:
        test_update_metadata(first_record_id)
    else:
        print("No record ID found for the first record. Skipping update test.")
    print("Step 3 Completed.\n")

    # 4. Test /delete_image for all records
    print("Step 4: Testing /delete_image for all records...")
    for record in all_records:
        record_id = record.get("id")
        if record_id:
            test_delete_image(record_id)
    print("Step 4 Completed.\n")

    print("All API Tests Completed.")
