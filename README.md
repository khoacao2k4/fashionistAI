<h1 align="center">
  <br>
  <img src="/img/logo.webp" alt="FashionistAI" width="200">
  <br>
  FashionistAI
  <br>
</h1>

FashionistAI is your personal fashion assistant designed to help you decide what to wear for any occasion. Whether it's an interview, a game day party, or a casual outing, FashionistAI uses the power of AI to provide style recommendations tailored to your wardrobe and the context you select.

---

## Key Features

### 1. **Add New Item**

- Snap a photo of your clothing item and upload it to your virtual wardrobe.
- Automatically classify items using a machine learning model based on:
  - Category (e.g., shirts, pants, dresses)
  - Season (e.g., summer, winter, all-season)
- Build and grow your wardrobe effortlessly.

### 2. **My Wardrobe**

- View and manage your clothing collection.
- Organize items by category, season, or personal tags.
- Access your wardrobe anytime, anywhere.

### 3. **Style Recommendations**

- Choose a context such as:
  - Formal
  - Casual
  - Party
  - ...
- Get personalized clothing suggestions from an AI model powered by GPT to match your selected occasion.
- Simplify your decision-making process with confidence and style.

---

## Tech Stack

### Backend

- **Flask**: Powers the API for managing wardrobe data and interfacing with the AI model.
- **MongoDB**: Stores user data, including wardrobe items and metadata.

### Machine Learning

- **Kaggle**: Trains the machine learning model for clothing classification.
- **OpenAI API**: Provides GPT-based recommendations for style contexts.

### Frontend

- **React Native**: Delivers a cross-platform mobile app experience, allowing users to access their wardrobe and receive recommendations on the go.

---

## Getting Started

### Prerequisites

- Install [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/).
- Install [Python](https://www.python.org/) and [pip](https://pip.pypa.io/).
- Set up a MongoDB instance (local or cloud).
- Obtain an API key from OpenAI.

### Installation

1. Clone the repository:

   ```bash
   https://github.com/khoacao2k4/fashionistAI.git
   ```

2. Navigate to the project directory:

   ```bash
   cd FashionistAI
   ```

3. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

5. Configure environment variables:

   - Create a `.env` file in the backend directory with:
     ```env
     MONGO_URI=your_mongodb_connection_string
     DB_NAME=your_db_name
     OPENAI_API_KEY=your_openai_api_key
     ```

### Running the Application

#### Backend

1. Start the Flask server:
   ```bash
   python app.py
   ```

#### Frontend

2. Start the React Native app:

   ```bash
   npm start
   ```

3. Follow the instructions to launch the app on an emulator or a physical device.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions or feedback, please reach out to [cqnhatkhoa@gmail.com](mailto\:cqnhatkhoa@gmail.com) or [sohamvazirani@gmail.com](mailto:sohamvazirani@gmail.com).

---

FashionistAI - Empowering your style, one outfit at a time!

