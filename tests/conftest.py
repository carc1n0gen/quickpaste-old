import pytest
from app import repositories
from app.create_app import create_app
from .mocks import MockMongoClient


@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    monkeypatch.setattr(repositories, 'MongoClient', MockMongoClient)
    yield


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.debug = True
    app.config['WTF_CSRF_ENABLED'] = False
    yield app


@pytest.fixture
def client(app):
    yield app.test_client()
