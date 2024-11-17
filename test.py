import requests
import json

# Base URL for the Flask API
BASE_URL = "http://127.0.0.1:5000"

# Test image file path
TEST_IMAGE_PATH = "test/1.jpg"

def test_predict():
    """
    Test the /predict API.
    """
    url = f"{BASE_URL}/predict"
    with open(TEST_IMAGE_PATH, "rb") as img_file:
        files = {"file": img_file}
        response = requests.post(url, files=files)
        print(f"Testing /predict...")
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
    return response.json() if response.status_code == 200 else None

def test_update_metadata(image_id):
    """
    Test the /update_metadata API.
    """
    url = f"{BASE_URL}/update_metadata"
    payload = {
        "image_id": image_id,
        "subCategory": "Updated Category",
        "articleType": "Updated Type",
        "gender": "Updated Gender",
        "baseColour": "Updated Colour",
        "season": "Updated Season",
        "usage": "Updated Usage"
    }
    response = requests.put(url, json=payload)
    print(f"Testing /update_metadata...")
    print(f"Status Code: {response.status_code}")
    return response.status_code == 200

def test_delete_image(image_id):
    """
    Test the /delete_image API.
    """
    url = f"{BASE_URL}/delete_image"
    payload = {
        "image_id": image_id
    }
    response = requests.delete(url, json=payload)
    print(f"Testing /delete_image...")
    print(f"Status Code: {response.status_code}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Starting API Tests...\n")

    # Test /predict API
    predict_response = test_predict()
    if not predict_response:
        print("Skipping further tests as /predict failed.")
        exit(1)

    # Test /get_all API
    all_records = test_get_all()
    if not all_records or len(all_records) == 0:
        print("No records found in /get_all. Skipping further tests.")
        exit(1)

    # Get the image_id of the first record
    image_id = all_records[0].get("image_id")
    print(f"Using image_id for update and delete: {image_id}")
    if not image_id:
        print("No image_id found in the records. Skipping further tests.")
        exit(1)

    # Test /update_metadata API
    if not test_update_metadata(image_id):
        print("Update metadata test failed. Continuing with delete test...")

    # Test /delete_image API
    if not test_delete_image(image_id):
        print("Delete image test failed.")
    else:
        print("Delete image test succeeded.")

    print("\nAPI Tests Completed.")
