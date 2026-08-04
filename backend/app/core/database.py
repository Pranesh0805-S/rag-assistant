from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongo_uri)
db = client["documind"]

users_collection = db["users"]