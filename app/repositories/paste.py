import time
import hashlib
from app.util import about_text
from app.repositories import db


def insert_paste(text):
    hash = hashlib.md5(text.encode('utf-8'))
    result = db.engine.execute(
        "SELECT * FROM pastes WHERE hash = ?", [hash.digest()])
    if result.first() is None:
        db.engine.execute("INSERT INTO pastes VALUES (?, ?, ?)",
                          [hash.digest(), text, time.time()])
    result.close()
    return hash.hexdigest()


def get_paste(hexhash):
    if hexhash == 'about':
        return about_text, None

    try:
        binhash = bytes.fromhex(hexhash)
    except (ValueError, TypeError):
        return None, None
    result = db.engine.execute(
        'SELECT * FROM pastes WHERE hash=?', [binhash])
    item = result.first()
    if item is None:
        return None, None
    result.close()
    return item[1], item[2]
