import logging
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError

from shared.config import get_mongo_config


class MongoConnection:
    _instance: Optional['MongoConnection'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.mongo_config = get_mongo_config()
            cls.host = cls.mongo_config.get("HOST", "localhost")
            cls.port = int(cls.mongo_config.get("PORT", 27017))
            cls.database_name = cls.mongo_config.get("DB_NAME", "InfluencersMarketing")
            try:
                # Creating client
                cls.client = MongoClient(cls.host, cls.port, serverSelectionTimeoutMS=5000)

                # Testing the connection
                cls.client.admin.command('ping')

                cls.database = cls.client[cls.database_name]
                cls.collection = cls.database[cls.mongo_config.get("INFLUENCERS_COLLECTION")]
                cls.posts = cls.database[cls.mongo_config.get("POSTS_COLLECTION")]

                logging.info("MongoDB connection established successfully")
            except (ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError) as e:
                cls._instance = None
                logging.error(f"Could not connect to MongoDB: {e}")
                raise

        return cls._instance

    def get_database(self):
        if self.database is not None:
            return self.database
        else:
            logging.error("Database connection is not established")
            raise ConnectionFailure("Database connection is not established")


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
