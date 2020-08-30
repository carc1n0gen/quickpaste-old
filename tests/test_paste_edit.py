from datetime import datetime
from flask import session
from app.repositories import paste


def test_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_prefil_text_when_clone_id_exists(client, monkeypatch):
    def mock_func(id):
        return {
            '_id': id,
            'created_at': datetime.utcnow(),
            'delete_at': datetime.utcnow(),
            'text': 'foobar'
        }
    monkeypatch.setattr(paste, 'get_paste', mock_func)

    response = client.get('/?clone=buzz')
    assert response.status_code == 200
    assert b'foobar' in response.data


def test_should_404_when_clone_id_is_not_found(client, monkeypatch):
    def mock_func(id):
        return None
    monkeypatch.setattr(paste, 'get_paste', mock_func)

    response = client.get('/?clone=buzz')
    assert response.status_code == 404


def should_redirect_when_edit_id_not_in_session(client, monkeypatch):
    response = client.get('/?edit=buzz')
    assert response.status_code == 302
    assert response.header['Location'] == 'http://localhost/buzz'


def test_should_prefill_text_when_edit_id_exists(client, monkeypatch):
    def mock_func(id):
        return {
            '_id': id,
            'created_at': datetime.utcnow(),
            'delete_at': datetime.utcnow(),
            'text': 'foobar'
        }
    monkeypatch.setattr(paste, 'get_paste', mock_func)

    with client.session_transaction() as sess:
        sess['created_ids'] = ['buzz']

    response = client.get('/?edit=buzz')
    assert response.status_code == 200
    assert b'foobar' in response.data


def test_should_404_when_edit_id_is_not_found(client, monkeypatch):
    def mock_func(id):
        return None
    monkeypatch.setattr(paste, 'get_paste', mock_func)

    with client.session_transaction() as sess:
        sess['created_ids'] = ['buzz']

    response = client.get('/?edit=buzz')
    assert response.status_code == 404


def test_should_redirect_to_show(client, monkeypatch):
    def mock_func(d):
        return 'foobar'
    monkeypatch.setattr(paste, 'upsert_paste', mock_func)

    with client as c:
        response = c.post('/', data={'text': 'sup dog', 'extension': ''})
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/foobar'
        assert session.get('created_ids') == ['foobar']


def test_should_rerender_edit(client):
    response = client.post('/')
    assert response.status_code == 200
    assert b'This field is required' in response.data
