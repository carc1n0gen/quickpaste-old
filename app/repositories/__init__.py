from pymongo import MongoClient
from flask import g, current_app


def get_mongo() -> MongoClient:
    if 'mongo' not in g:
        g.mongo = MongoClient(
            current_app.config.get('MONGO_HOST', '127.0.0.1'),
            current_app.config.get('MONGO_PORT', 27017)
        )
    return g.mongo


def insert_one(collection: str, d: dict):
    db_name = current_app.config.get('MONGO_DATABASE', 'quickpaste')
    mongo = get_mongo()
    return mongo[db_name][collection].insert_one(d).inserted_id


def find_one(collection: str, d: dict):
    db_name = current_app.config.get('MONGO_DATABASE', 'quickpaste')
    mongo = get_mongo()
    return mongo[db_name][collection].find_one(d)
