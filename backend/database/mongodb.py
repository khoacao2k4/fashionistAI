from pymongo import MongoClient
import gridfs
from config import MONGO_URI, DB_NAME

client = None
db = None
fs = None

def init_db():
    global client, db, fs
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    fs = gridfs.GridFS(db)