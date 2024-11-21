from flask import Blueprint, request, jsonify
from bson import ObjectId
from database.mongodb import db, fs
import base64

# Define the blueprint
bp = Blueprint("crud", __name__)

@bp.route('/get_all', methods=['GET'])
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
                "baseColour": item.get("baseColour"),
                "season": item.get("season"),
                "usage": item.get("usage"),
                "image": image_base64  # Include the base64 image
            })

        return jsonify(all_items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/update_metadata', methods=['PUT'])
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
    
@bp.route('/delete_image', methods=['DELETE'])
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