from datetime import datetime
from flask import current_app
from app.util import get_random_string
from . import insert_one, find_one


def insert_paste(text: str) -> str:
    length = current_app.config.get('PASTE_ID_LENGTH', 7)
    return insert_one('pastes', {
        '_id': get_random_string(length),
        'text': text,
        'created_at': datetime.utcnow()
    })


def get_paste(id):
    doc = find_one('pastes', {'_id': id})
    if doc is None:
        return None, None
    return doc['text'], doc['created_at']
