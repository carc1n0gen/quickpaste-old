import hashlib
from datetime import datetime, timedelta
from app.repositories import db
from app.commands import cleanup_factory


def test_should_cleanup_old_pastes(app, client):
    with app.app_context():
        text = 'foo'
        hash = hashlib.md5(text.encode('utf-8'))
        week_ago_and_one_day = datetime.now() - timedelta(weeks=1, days=1)
        db.engine.execute(
            "INSERT INTO pastes (hash, text, timestamp) VALUES (?, ?, ?)",
            [hash.digest(), text, week_ago_and_one_day.timestamp()]
        )

        runner = app.test_cli_runner()
        command = cleanup_factory(app)
        runner.invoke(command)

        result = db.engine.execute('SELECT count(timestamp) FROM pastes')
        assert result.scalar() == 0
