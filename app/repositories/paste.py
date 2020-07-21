from datetime import datetime, timedelta
from flask import current_app
from . import update_one, find_one, delete_one, make_id


def upsert_paste(updates: dict):
    paste_life_in_seconds = current_app.config.get(
        'PASTE_EXPIRE_AFTER_SECONDS', 604800
    )
    created_at = updated_at = datetime.utcnow()
    delete_at = created_at + timedelta(seconds=paste_life_in_seconds)

    defaults = {
        '_id': make_id(),
        'created_at': created_at,
        'delete_at': delete_at
    }

    merged = {**defaults, **updates, 'updated_at': updated_at}
    update_one(
        'pastes',
        {
            '_id': merged['_id']
        },
        {
            '$set': merged
        },
        upsert=True
    )
    return merged['_id']


def get_paste(id):
    return find_one('pastes', {'_id': id})


def delete_paste(id):
    return delete_one('pastes', {'_id': id})
