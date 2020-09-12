from app import repositories
from app.repositories import paste
from ..mocks import MockMongoClient


def test_should_return_data_when_in_db(app, monkeypatch):
    monkeypatch.setattr(repositories, 'MongoClient', MockMongoClient)

    with app.app_context():
        doc = paste.get_paste('abcd')
        assert doc is not None
        assert doc['_id'] == 'abcd'


def test_should_return_none_when_not_in_db(app, monkeypatch):
    monkeypatch.setattr(repositories, 'MongoClient', MockMongoClient)

    with app.app_context():
        doc = paste.get_paste('1234')
        assert doc is None
