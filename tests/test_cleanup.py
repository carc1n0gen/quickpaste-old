import hashlib
from datetime import datetime, timedelta
from app import app, db, cleanup


def test_should_cleanup_old_pastes(client):
    text = 'foo'
    hash = hashlib.md5(text.encode('utf-8'))
    week_ago_and_one_day = datetime.now() - timedelta(weeks=1, days=1)
    db.engine.execute("INSERT INTO pastes VALUES (?, ?, ?)",
                      [hash.digest(), text, week_ago_and_one_day.timestamp()])

    runner = app.test_cli_runner()
    runner.invoke(cleanup)

    result = db.engine.execute('SELECT count(timestamp) FROM pastes')
    assert result.scalar() == 0
