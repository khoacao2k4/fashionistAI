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
import openai

######################################## MACHINE LEARNING MODULE ########################################
# Paths
LABEL_CLASSES_PATH = "model/label_classes.json"
MODEL_PATH = "model/clothes_classifier_new.h5"
IMAGE_DIMS = (60, 60, 3)
# Load label classes
with open(LABEL_CLASSES_PATH, "r") as json_file:
    LABEL_CLASSES = json.load(json_file)

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

# ======================================== CHATGPT MODULE =====================================
class FashionDatasetRecommenderChatGPT:
    def __init__(self, openai_api_key: str):
        """
        Initializes the recommendation system using ChatGPT API.

        :param openai_api_key: OpenAI API key for accessing ChatGPT.
        """
        # Initialize OpenAI API
        openai.api_key = openai_api_key
        print("OpenAI API initialized.")

    def recommend(self, clothes: list, occasion: str, n: int = 5):
        """
        Recommend similar items using the OpenAI API.

        :param clothes: List of clothing items with their attributes.
        :param occasion: The occasion type to filter items (e.g., casual, formal, sports).
        :param n: Number of recommendations to return.
        :return: JSON containing recommendations or an error message.
        """
        # Prepare a prompt for ChatGPT
        prompt = [
            {"role": "system", "content": "You are a professional fashion recommendation assistant who provides detailed, personalized, and persuasive fashion advice."},
            {"role": "user", "content": f"""
                Based on the following clothing items:
                {json.dumps(clothes, indent=2)}

                Recommend {n} items whose attributes and style match the occasion: {occasion}. If there are less than {n} recommendations, you can list them all but no duplicates.
                Each identifier should be exactly the same as the ID of the target item, and only appear once. Each recommendation should include:
                - "id": The ID from item's metadata. Must be exactly the same as the ID of the target item.
                - "description": A persuasive explanation of why this item is a great choice for the occasion, highlighting its features, aesthetics, and how it complements the context. Limit the range to 20-40 words.

                Ensure the descriptions are detailed and highlight how each recommendation enhances the user's style and confidence. Provide the output strictly in valid JSON format, ensuring it is ready for JSON parsing. Example format:
                {{
                    "recommendations": [
                        {{"id": 1, "description": "This is a stunning choice because..."}},
                        {{"id": 2, "description": "This fits perfectly for the occasion due to..."}}
                    ]
                }}
            """}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=prompt,
                max_tokens=300,
                temperature=0.7
            )
            # Extract and return the recommendations
            recommendations = response['choices'][0]['message']['content'].strip()
            return json.loads(recommendations)
        except Exception as e:
            return {"error": f"Error during OpenAI API call: {e}"}

# Initialize the recommender
openai_api_key = "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"
recommender = FashionDatasetRecommenderChatGPT(openai_api_key=openai_api_key)


# ======================================== MONGODB MODULE =====================================
# MongoDB configuration
mongo_uri = "mongodb+srv://caokhoamickey:L4pe2CQcROwp41Kc@fashionistaidb.v0d14.mongodb.net/?retryWrites=true&w=majority&appName=FashionistaiDB"
db_name = "FashionistaiDB"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]
fs = gridfs.GridFS(db)


# ======================================== FLASK MODULE =====================================
# Flask app initialization
app = Flask(__name__)

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
        print("Prediction Result:", output)
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
                "id": str(item.get("_id")),  # Convert ObjectId to string
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
        if not data or "id" not in data:
            return jsonify({"error": "Missing 'id' in request"}), 400
        
        image_id = data["id"]

        # Validate and convert image_id
        if not ObjectId.is_valid(image_id):
            return jsonify({"error": "Invalid 'id' format"}), 400
        object_id = ObjectId(image_id)

        # Extract new metadata
        new_metadata = {k: v for k, v in data.items() if k != "id"}
        if not new_metadata:
            return jsonify({"error": "No metadata provided for update"}), 400

        # Update metadata in MongoDB
        result = db.clothes.update_one({"_id": object_id}, {"$set": new_metadata})

        if result.matched_count == 0:
            return jsonify({"error": "No record found with the specified 'id'"}), 404
        
        return jsonify({"message": "Metadata updated successfully"}), 200

    except Exception as e:
        print(f"Error in update_metadata: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_image', methods=['DELETE'])
def delete_image():
    try:
        data = request.json
        print(data)
        if not data or "id" not in data:
            return jsonify({"error": "Missing 'id' in request"}), 400
        
        image_id = data["id"]

        # Validate and convert image_id
        if not ObjectId.is_valid(image_id):
            return jsonify({"error": "Invalid 'id' format"}), 400
        object_id = ObjectId(image_id)

        # Check if the record exists
        record = db.clothes.find_one({"_id": object_id})
        if not record:
            return jsonify({"error": "No record found with the specified 'id'"}), 404

        # Remove the image from GridFS
        fs.delete(record.get("image"))

        # Remove the metadata from the database
        db.clothes.delete_one({"_id": object_id})

        return jsonify({"message": "Image and metadata removed successfully"}), 200

    except Exception as e:
        print(f"Error in delete_image: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint for fetching fashion recommendations."""
    data = request.json

    # Extract input parameters from the request
    clothes = data.get('clothes')
    occasion = data.get('occasion')
    n = data.get('n', 5)  # Default to 5 recommendations

    if not clothes or not occasion:
        return jsonify({"error": "Missing required parameters: clothes and occasion."}), 400
    print(clothes)
    print(occasion)
    print(n)
    # Fetch recommendations
    result = recommender.recommend(clothes=clothes, occasion=occasion, n=n)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
