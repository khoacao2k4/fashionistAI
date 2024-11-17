from flask import Flask, request, jsonify
import os
import cv2
import json
from keras.applications.resnet import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
from pymongo import MongoClient
import gridfs
import base64
from bson import ObjectId

# MongoDB configuration
mongo_uri = "mongodb+srv://caokhoamickey:L4pe2CQcROwp41Kc@fashionistaidb.v0d14.mongodb.net/?retryWrites=true&w=majority&appName=FashionistaiDB"
db_name = "FashionistaiDB"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]
fs = gridfs.GridFS(db)

# Flask app initialization
app = Flask(__name__)

# Paths
LABEL_CLASSES_PATH = "model/label_classes.json"
MODEL_PATH = "model/clothes_classifier.h5"
IMAGE_DIMS = (60, 60, 3)

# Load label classes
with open(LABEL_CLASSES_PATH, "r") as json_file:
    LABEL_CLASSES = json.load(json_file)

# ========================================MACHINE LEARNING MODEL=====================================
# Classification Model Class
class ClassificationModel:
    def __init__(self):
        print("====== Initializing Model ======")
        self.model = None

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = preprocess_input(image)
        return image

    def load(self, model_path):
        print("====== Loading Model ======")
        self.model = load_model(model_path)

    def predict(self, image_path):
        print("====== Load Image ======")
        image = self.load_image(image_path)
        image_data = np.expand_dims(image, axis=0)

        print("====== Predict ======")
        (subCategoryProba, articleProba, genderProba, colorProba, seasonProba, usageProba) = self.model.predict(image_data)

        subCategoryIdx = subCategoryProba[0].argmax()
        articleIdx = articleProba[0].argmax()
        genderIdx = genderProba[0].argmax()
        colorIdx = colorProba[0].argmax()
        seasonIdx = seasonProba[0].argmax()
        usageIdx = usageProba[0].argmax()

        subCategoryLabel = LABEL_CLASSES["subCategory"][subCategoryIdx]
        articleLabel = LABEL_CLASSES["articleType"][articleIdx]
        genderLabel = LABEL_CLASSES["gender"][genderIdx]
        colorLabel = LABEL_CLASSES["baseColour"][colorIdx]
        seasonLabel = LABEL_CLASSES["season"][seasonIdx]
        usageLabel = LABEL_CLASSES["usage"][usageIdx]

        return {
            "subCategory": subCategoryLabel,
            "articleType": articleLabel,
            "gender": genderLabel,
            "baseColour": colorLabel,
            "season": seasonLabel,
            "usage": usageLabel
        }

# Initialize model
learner = ClassificationModel()
learner.load(MODEL_PATH)

# ========================================MONGODB MODEL=====================================
def save_to_mongodb(image_path, prediction):
    """
    Save the image and prediction results to MongoDB.
    :param image_path: Path to the image file.
    :param prediction: Dictionary containing prediction results.
    """
    with open(image_path, "rb") as img_file:
        # Store the image in GridFS
        image_id = fs.put(img_file, filename=os.path.basename(image_path))
    
    # Store the metadata in the database
    document = {
        "image": image_id,  # Reference to the GridFS image
        "subCategory": prediction["subCategory"],
        "article": prediction["articleType"],
        "gender": prediction["gender"],
        "color": prediction["baseColour"],
        "season": prediction["season"],
        "usage": prediction["usage"]
    }
    db.clothes.insert_one(document)
    print(f"Saved to MongoDB with image_id: {image_id}")



# ========================================FLASK MODEL=====================================
# Define Flask routes
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle the prediction request.
    Expects an image file in the POST request.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    try:
        # Run prediction using the model
        output = learner.predict(temp_path)
        
        # Save to MongoDB
        save_to_mongodb(temp_path, output)
        
        # Clean up temporary file
        os.remove(temp_path)
        return jsonify(output)
    except Exception as e:
        os.remove(temp_path)  # Clean up temporary file in case of error
        return jsonify({"error": str(e)}), 500

@app.route('/get_all', methods=['GET'])
def get_all():
    """
    Fetch all clothes data from the database, including images and image_id.
    """
    try:
        clothes = db.clothes.find()
        all_items = []

        for item in clothes:
            image_id = item.get("image")  # Get the GridFS image ID
            image_file = fs.get(image_id)  # Fetch the image from GridFS

            # Convert the image to a base64 string
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            # Append document with image_id and metadata to the list
            all_items.append({
                "image_id": str(item.get("image")),  # Convert ObjectId to string
                "subCategory": item.get("subCategory"),
                "article": item.get("article"),
                "gender": item.get("gender"),
                "color": item.get("baseColour"),
                "season": item.get("season"),
                "usage": item.get("usage"),
                "image": image_base64  # Include the base64 image
            })

        return jsonify(all_items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_metadata', methods=['PUT'])
def update_metadata():
    try:
        data = request.json
        if not data or "image_id" not in data:
            return jsonify({"error": "Missing 'image_id' in request"}), 400
        
        image_id = data["image_id"]

        # Validate and convert image_id
        if not ObjectId.is_valid(image_id):
            return jsonify({"error": "Invalid 'image_id' format"}), 400
        object_id = ObjectId(image_id)

        # Extract new metadata
        new_metadata = {k: v for k, v in data.items() if k != "image_id"}
        if not new_metadata:
            return jsonify({"error": "No metadata provided for update"}), 400

        # Update metadata in MongoDB
        result = db.clothes.update_one({"image": object_id}, {"$set": new_metadata})

        if result.matched_count == 0:
            return jsonify({"error": "No record found with the specified 'image_id'"}), 404
        
        return jsonify({"message": "Metadata updated successfully"}), 200

    except Exception as e:
        print(f"Error in update_metadata: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_image', methods=['DELETE'])
def delete_image():
    try:
        data = request.json
        if not data or "image_id" not in data:
            return jsonify({"error": "Missing 'image_id' in request"}), 400
        
        image_id = data["image_id"]

        # Validate and convert image_id
        if not ObjectId.is_valid(image_id):
            return jsonify({"error": "Invalid 'image_id' format"}), 400
        object_id = ObjectId(image_id)

        # Check if the record exists
        record = db.clothes.find_one({"image": object_id})
        if not record:
            return jsonify({"error": "No record found with the specified 'image_id'"}), 404

        # Remove the image from GridFS
        fs.delete(object_id)

        # Remove the metadata from the database
        db.clothes.delete_one({"image": object_id})

        return jsonify({"message": "Image and metadata removed successfully"}), 200

    except Exception as e:
        print(f"Error in delete_image: {e}")
        return jsonify({"error": str(e)}), 500


# @app.route('/test_decode', methods=['GET'])
# def test_decode():
#     """
#     Fetch one item, decode its image from base64, and save it locally to verify.
#     """
#     try:
#         # Fetch one document from the clothes collection
#         item = db.clothes.find_one()
#         if not item:
#             return jsonify({"error": "No documents found in the database"}), 404

#         image_id = item.get("image")  # Get the GridFS image ID
#         if not image_id:
#             return jsonify({"error": "No image found for this item"}), 404
        
#         # Fetch the image from GridFS
#         image_file = fs.get(image_id)
        
#         # Convert the image to a base64 string
#         image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

#         # Decode the base64 string back to binary
#         image_data = base64.b64decode(image_base64)
        
#         # Save the decoded image locally
#         output_path = os.path.join("temp", "decoded_image.jpg")
#         os.makedirs("temp", exist_ok=True)  # Ensure the temp directory exists
#         with open(output_path, "wb") as f:
#             f.write(image_data)

#         return jsonify({"message": "Image decoded and saved successfully", "output_path": output_path}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
