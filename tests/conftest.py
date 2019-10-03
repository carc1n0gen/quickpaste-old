import pytest

from app.create_app import create_app, limiter, alembic, db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['MAX_PASTE_LENGTH'] = 20
    app.debug = False
    yield app


@pytest.fixture
def client(app):
    limiter.enabled = False
    with app.app_context():
        alembic.upgrade('head')
        db.engine.execute('DELETE FROM pastes')
    client = app.test_client()
    yield client
