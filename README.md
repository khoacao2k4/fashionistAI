###FashionistAI

FashionistAI is your personal fashion assistant designed to help you decide what to wear for any occasion. Whether it's an interview, a game day party, or a casual outing, FashionistAI uses the power of AI to provide style recommendations tailored to your wardrobe and the context you select.

###Key Features

#1. Add New Item

Snap a photo of your clothing item and upload it to your virtual wardrobe.

Automatically classify items using a machine learning model based on:

Category (e.g., shirts, pants, dresses)

Season (e.g., summer, winter, all-season)

Build and grow your wardrobe effortlessly.

#2. My Wardrobe

View and manage your clothing collection.

Organize items by category, season, or personal tags.

Access your wardrobe anytime, anywhere.

#3. Style Recommendations

Choose a context such as:

Formal

Casual

Party

Get personalized clothing suggestions from an AI model powered by GPT to match your selected occasion.

Simplify your decision-making process with confidence and style.

###Tech Stack

#Backend

Flask: Powers the API for managing wardrobe data and interfacing with the AI model.

MongoDB: Stores user data, including wardrobe items and metadata.

#Machine Learning

Kaggle: Trains the machine learning model for clothing classification.

OpenAI API: Provides GPT-based recommendations for style contexts.

#Frontend

React Native: Delivers a cross-platform mobile app experience, allowing users to access their wardrobe and receive recommendations on the go.

###Getting Started

#Prerequisites

Install Node.js and npm.

Install Python and pip.

Set up a MongoDB instance (local or cloud).

Obtain an API key from OpenAI.

#Installation

Clone the repository:

git clone https://github.com/yourusername/FashionistAI.git

Navigate to the project directory:

cd FashionistAI

Install backend dependencies:

pip install -r requirements.txt

Install frontend dependencies:

cd frontend
npm install

Configure environment variables:

Create a .env file in the backend directory with:

MONGO_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key

#Running the Application

Backend

Start the Flask server:

python app.py

Frontend

Start the React Native app:

npm start

Follow the instructions to launch the app on an emulator or a physical device.

License

This project is licensed under the MIT License.

Contact

For questions or feedback, please reach out to your_email@example.com.

FashionistAI - Empowering your style, one outfit at a time!

