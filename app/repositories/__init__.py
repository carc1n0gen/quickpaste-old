import random
from werkzeug.local import LocalProxy
from pymongo import MongoClient
from flask import g, current_app


def get_mongo_client():
    if 'mongo_client' not in g:
        g.mongo_client = MongoClient(
            current_app.config.get('MONGO_HOST', '127.0.0.1'),
            current_app.config.get('MONGO_PORT', 27017),
            serverSelectionTimeoutMS=5000
        )
    return g.mongo_client


def get_database():
    if 'database' not in g:
        g.database = mongo_client[current_app.config.get('MONGO_DATABASE', 'quickpaste')]
    return g.database


mongo_client = LocalProxy(get_mongo_client)
database = LocalProxy(get_database)


def get_random_string(length, alphabet):
    r = random.SystemRandom()
    alphabet_len = len(alphabet)
    s = [alphabet[r.randrange(alphabet_len)] for i in range(length)]
    return ''.join(s)


def make_id():
    length = current_app.config.get('PASTE_ID_LENGTH', 7)
    alphabet = current_app.config.get(
        'LINK_ALPHABET',
        'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-'
    )
    return get_random_string(length, alphabet)


def update_one(collection: str, query: dict, updates: dict, upsert=False):
    return database[collection].update_one(query, updates, upsert=upsert)


def find_one(collection: str, d: dict):
    return database[collection].find_one(d)


def delete_one(collection: str, d: dict):
    return database[collection].delete_one(d)
