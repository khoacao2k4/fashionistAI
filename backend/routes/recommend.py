from flask import Blueprint, request, jsonify
from database.mongodb import db
from model.recommender import FashionDatasetRecommenderChatGPT

bp = Blueprint("recommend", __name__)
recommender = FashionDatasetRecommenderChatGPT()

bp.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint for fetching fashion recommendations."""
    data = request.json

    # Extract input parameters from the request
    # Call the get_all() function to fetch all clothes data
    clothes = []
    clothes_cursor = db.clothes.find()
    for item in clothes_cursor:    # Append document with image_id and metadata to the list
        clothes.append({
            "id": str(item.get("_id")),  # Convert ObjectId to string
            "subCategory": item.get("subCategory"),
            "typeOfClothing": item.get("article"),
            "gender": item.get("gender"),
            "baseColour": item.get("baseColour"),
            "season": item.get("season"),
            "usage": item.get("usage")
        })
    print(clothes)
    occasion = data.get('occasion')
    n = data.get('n', 5)  # Default to 5 recommendations
    print(n)
    if not clothes or not occasion:
        return jsonify({"error": "Missing required parameters: clothes and occasion."}), 400
    # Fetch recommendations
    result = recommender.recommend(clothes=clothes, occasion=occasion, n=n)
    return jsonify(result)

# @app.route('/recommend_old', methods=['POST'])
# def recommend_old():
#     """Endpoint for fetching fashion recommendations."""
#     data = request.json

#     # Extract input parameters from the request
#     clothes = data.get('clothes')
#     occasion = data.get('occasion')
#     n = data.get('n', 5)  # Default to 5 recommendations

#     if not clothes or not occasion:
#         return jsonify({"error": "Missing required parameters: clothes and occasion."}), 400
#     print(clothes)
#     print(occasion)
#     print(n)
#     # Fetch recommendations
#     result = recommender.recommend(clothes=clothes, occasion=occasion, n=n)
#     return jsonify(result)