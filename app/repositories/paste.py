from typing import Callable
from datetime import datetime, timedelta
from flask import current_app
from . import insert_one, find_one, delete_one, make_id


def insert_paste(text: str, make_id_fn: Callable = make_id) -> str:
    paste_life_in_seconds = current_app.config.get(
        'PASTE_EXPIRE_AFTER_SECONDS', 604800
    )
    created_at = datetime.utcnow()
    delete_at = created_at + timedelta(seconds=paste_life_in_seconds)
    return insert_one('pastes', {
        '_id': make_id_fn(),
        'text': text,
        'created_at': created_at,
        'delete_at': delete_at
    })


def get_paste(id):
    return find_one('pastes', {'_id': id})


def delete_paste(id):
    return delete_one('pastes', {'_id': id})
