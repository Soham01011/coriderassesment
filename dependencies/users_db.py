'''from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
database = client['coriderassesment']
users_collection = database['users']
'''

from pymongo import MongoClient, errors
from bson import ObjectId
import logging

MONGO_URI = "mongodb://localhost:27017"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    client = MongoClient(MONGO_URI)
    database = client['coriderassesment']
    users_collection = database['users']
    logger.info("successfully conented to the mongodb")
except errors.ConnectionFailure as e:
    logging.error(f"Falied to connect :{e}")
    client ,database,users_collection = None, None,None