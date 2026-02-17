import logging

from shared.config import get_mongo_config
from shared.mongo import MongoConnection


class InfluencersService:
    def __init__(self, mongo_connection: MongoConnection):
        db = mongo_connection.get_database()
        mongo_config = get_mongo_config()

        self.posts_collection = db[mongo_config.get("POSTS_COLLECTION", "posts")]
        self.influencers_collection = db[mongo_config.get("INFLUENCERS_COLLECTION", "Influencers")]

    def get_influencers(self):
        try:
            influencers = list(self.influencers_collection.find())
            logging.info("Fetched %d influencers", len(influencers))
            return influencers
        except Exception as e:
            logging.error("An error occurred while fetching influencers: %s", str(e))
            return []

    def get_bio_documents(self, noise_words: set[str] | None = None) -> list[str]:
        """Build a list of text documents from influencer bios + categories.

        Each document is the concatenation of the influencer's Bio and Category
        (when they are not ``"NULL"``).  Optional *noise_words* are stripped from
        every document before it is added to the result.

        Returns:
            A list of non-empty document strings ready for topic modelling.
        """
        if noise_words is None:
            noise_words = set()
        influencers = self.get_influencers()
        docs: list[str] = []
        for influencer in influencers:
            doc = ""
            if influencer.get("Bio", "NULL") != "NULL":
                doc += influencer["Bio"]
            if influencer.get("Category", "NULL") != "NULL":
                doc += " " + influencer["Category"]
            if doc.strip():
                for w in noise_words:
                    doc = doc.replace(w, "")
                docs.append(doc)
        logging.info("Built %d bio documents", len(docs))
        return docs

    def get_posts(self):
        try:
            posts = list(self.posts_collection.find())
            logging.info("Fetched %d posts", len(posts))
            return posts
        except Exception as e:
            logging.error("An error occurred while fetching posts: %s", str(e))
            return []

    def update_influencer(self, influencer, key, value):
        try:
            query = {'_id': influencer['_id']}
            update = {'$set': {key: value}}
            result = self.influencers_collection.update_one(query, update)
            if result.modified_count > 0:
                logging.info("Updated influencer %s with %s: %s", influencer['_id'], key, value)
            else:
                logging.warning("No influencer found with id %s to update", influencer['_id'])
            return result
        except Exception as e:
            logging.error("An error occurred while updating an influencer: %s", str(e))
            return None

    def update_post(self, post, key, value):
        try:
            query = {'_id': post['_id']}
            update = {'$set': {key: value}}
            result = self.posts_collection.update_one(query, update)
            if result.modified_count > 0:
                logging.info("Updated post %s with %s: %s", post['_id'], key, value)
            else:
                logging.warning("No post found with id %s to update", post['_id'])
            return result
        except Exception as e:
            logging.error("An error occurred while updating a post: %s", str(e))
            return None
