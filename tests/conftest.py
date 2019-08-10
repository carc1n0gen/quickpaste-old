import pytest

from app import app, limiter, alembic, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['MAX_PASTE_LENGTH'] = 20
    limiter.enabled = False
    with app.app_context():
        alembic.upgrade('head')
    db.engine.execute('DELETE FROM pastes')
    client = app.test_client()
    yield client
