import time
import hashlib
from app.util import about_text
from app.repositories import db
from app.shortlink import shortlink


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
    if id == 'about':
        return about_text, None
    int_id = None

    try:
        binhash = bytes.fromhex(id)
    except (ValueError, TypeError):
        try:
            # TODO: Once I no longer need to support hexhash lookups, move this
            # decode outside the repository.
            int_id = shortlink.decode(id)
        except (ValueError, TypeError):
            return None, None

    if int_id:
        result = db.engine.execute(
            'SELECT text, timestamp FROM pastes WHERE id=?',
            [int_id]
        )
    else:
        result = db.engine.execute(
            'SELECT text, timestamp FROM pastes WHERE hash=?',
            [binhash]
        )

    item = result.first()
    result.close()
    if item is None:
        return None, None
    return item[0], item[1]
