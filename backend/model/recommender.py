import openai
import json
from config import OPENAI_API_KEY

class FashionDatasetRecommenderChatGPT:
    def __init__(self):
        """
        Initializes the recommendation system using ChatGPT API.
        """
        # Initialize OpenAI API
        openai.api_key = OPENAI_API_KEY
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