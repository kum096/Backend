import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection URI from your .env file (edit this there)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "tracknest_db")

# Create MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Access database
db = client[DB_NAME]

# Dependency function for FastAPI routes
def get_database():
    return db
