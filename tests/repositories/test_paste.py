from app import repositories
from app.repositories import paste
from ..mocks import MockMongoClient


def test_get_paste_happy_path(app, monkeypatch):
    monkeypatch.setattr(repositories, 'MongoClient', MockMongoClient)

    with app.app_context():
        doc = paste.get_paste('abcd')
        assert doc is not None
        assert doc['_id'] == 'abcd'


def test_get_paste_sad_path(app, monkeypatch):
    monkeypatch.setattr(repositories, 'MongoClient', MockMongoClient)

    with app.app_context():
        doc = paste.get_paste('1234')
        assert doc is None
