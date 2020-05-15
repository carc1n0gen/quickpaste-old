from datetime import datetime, timedelta
from flask import current_app
from app.util import get_random_string
from . import insert_one, find_one


def insert_paste(text: str) -> str:
    length = current_app.config.get('PASTE_ID_LENGTH', 7)
    paste_life_in_seconds = current_app.config.get(
        'PASTE_EXPIRE_AFTER_SECONDS', 604800
    )
    created_at = datetime.utcnow()
    delete_at = created_at + timedelta(seconds=paste_life_in_seconds)
    return insert_one('pastes', {
        '_id': get_random_string(length),
        'text': text,
        'created_at': created_at,
        'delete_at': delete_at
    })


def get_paste(id):
    return find_one('pastes', {'_id': id})
