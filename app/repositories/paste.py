import time
import hashlib
from app.util import about_text
from app.repositories import db


def insert_paste(text):
    hash = hashlib.md5(text.encode('utf-8'))
    result = db.engine.execute(
        "SELECT id FROM pastes WHERE hash = ?",
        [hash.digest()]
    )

    row = result.first()
    if row is None:
        result = db.engine.execute(
            "INSERT INTO pastes (hash, text, timestamp) VALUES (?, ?, ?)",
            [hash.digest(), text, time.time()]
        )
        id = result.lastrowid
    else:
        id = row[0]

    result.close()
    return id


def get_paste(id):
    try:
        if id == 'about':
            return about_text, None

        result = db.engine.execute(
            'SELECT text, timestamp FROM pastes WHERE id=?',
            [id]
        )

        item = result.first()
        result.close()
        if item is None:
            return None, None
        return item[0], item[1]

    except (ValueError, TypeError, OverflowError):
        return None, None
