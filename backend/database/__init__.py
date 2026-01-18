"""
Database Connection Management
===============================

MongoDB connection using Motor (async driver for FastAPI).

SETUP:
1. Install: pip install motor pymongo
2. Add to .env:
   MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB_NAME=synthframe

3. For local MongoDB:
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB_NAME=synthframe

USAGE:
    from backend.database import get_database, get_projects_collection
    
    db = await get_database()
    projects = get_projects_collection()
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional

from backend.config import settings


# Global client instance
_mongo_client: Optional[AsyncIOMotorClient] = None
_database: Optional[AsyncIOMotorDatabase] = None


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Get or create MongoDB client (singleton pattern).
    
    Returns:
        AsyncIOMotorClient instance
    """
    global _mongo_client
    
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
        )
    
    return _mongo_client


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get MongoDB database instance.
    
    Returns:
        AsyncIOMotorDatabase for synthframe
    """
    global _database
    
    if _database is None:
        client = get_mongo_client()
        _database = client[settings.mongodb_db_name]
    
    return _database


def get_projects_collection() -> AsyncIOMotorCollection:
    """
    Get the 'projects' collection (synchronous helper).
    
    Returns:
        Collection object for projects
    """
    client = get_mongo_client()
    db = client[settings.mongodb_db_name]
    return db["projects"]


async def close_mongo_connection():
    """
    Close MongoDB connection (call on app shutdown).
    """
    global _mongo_client, _database
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _database = None


async def ping_database() -> bool:
    """
    Check if MongoDB connection is working.
    
    Returns:
        True if connected, False otherwise
    """
    try:
        client = get_mongo_client()
        await client.admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
