from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "mydatabase"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# Define collections
user_collection = database.get_collection("users")
data_collection = database.get_collection("data")
chat_collection = database.get_collection("chats")
chat_logs_collection = database.get_collection("chat_logs")
