from flask import Blueprint, request, jsonify
import os
from database.mongodb import db, fs
from model.clothes_classifier import ClassificationModel

bp = Blueprint("predict", __name__)
classifier = ClassificationModel()

@bp.route('/predict', methods=['POST'])
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
        output = classifier.predict(temp_path)
        print("Prediction Result:", output)
        # Save to MongoDB
        save_to_mongodb(temp_path, output)
        # Clean up temporary file
        os.remove(temp_path)
        return jsonify(output)
    except Exception as e:
        os.remove(temp_path)  # Clean up temporary file in case of error
        return jsonify({"error": str(e)}), 500

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
        "baseColour": prediction["baseColour"],
        "season": prediction["season"],
        "usage": prediction["usage"]
    }
    db.clothes.insert_one(document)
    print(f"Saved to MongoDB with image_id: {image_id}")