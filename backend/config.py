import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the current file
# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "default_mongo_uri_here")
DB_NAME = os.getenv("DB_NAME", "FashionistaiDB")
# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default_openai_key_here")
# Paths
LABEL_CLASSES_PATH = os.path.join(BASE_DIR, "model/label_classes.json")
MODEL_PATH = os.path.join(BASE_DIR, "model/clothes_classifier.h5")