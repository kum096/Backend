import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
from typing import Generator

# Load environment variables from .env
load_dotenv()

# Load MongoDB connection settings
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "tracknest_db")

# Create the MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
database: AsyncIOMotorDatabase = client[MONGODB_DB_NAME]

# FastAPI dependency to get DB
async def get_database() -> AsyncIOMotorDatabase:
    return database
