from flask import session
from app.repositories import paste
from .mocks import mock_get_paste_factory


def test_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_prefill_text_when_clone_id_exists(client):
    response = client.get('/?clone=abcd')
    assert response.status_code == 200
    assert b'The cow goes mooooooo.' in response.data


def test_should_prefill_text_when_cloning_permanent_paste(client):
    response = client.get('/?clone=about')
    assert response.status_code == 200
    assert b'The about page.' in response.data


def test_should_404_when_clone_id_is_not_found(client):
    response = client.get('/?clone=1234')
    assert response.status_code == 404


def test_should_redirect_when_edit_id_not_in_session_get(client):
    response = client.get('/?edit=abcd')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/abcd'


def test_should_redirect_when_edit_id_not_in_session_post(client):
    response = client.post('/?edit=abcd')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/abcd'


def test_should_update_existing_paste(client, monkeypatch):
    # Revisit this, the mock upsert sort of doesnt make sense, its return doesnt matter at
    # this time
    def mock_upsert_func(d):
        return 'foobar'

    original_text = 'The cow goes mooooo.'
    updated_text = 'quack quack quack.'

    monkeypatch.setattr(paste, 'get_paste', mock_get_paste_factory('abcd', [
        original_text,
        updated_text
    ]))
    monkeypatch.setattr(paste, 'upsert_paste', mock_upsert_func)

    with client.session_transaction() as sess:
        sess['created_ids'] = ['abcd']

    response = client.post('/', data={'id': 'abcd', 'text': updated_text, 'extension': '', 'delete_after': '6'}, follow_redirects=True)
    assert response.status_code == 200
    assert updated_text.encode('utf-8') in response.data


def test_should_prefill_text_when_edit_id_exists(client, monkeypatch):
    with client.session_transaction() as sess:
        sess['created_ids'] = ['abcd']

    response = client.get('/?edit=abcd')
    assert response.status_code == 200
    assert b'The cow goes mooooooo.' in response.data


def test_should_404_when_edit_id_is_not_found(client, monkeypatch):
    with client.session_transaction() as sess:
        sess['created_ids'] = ['1234']

    response = client.get('/?edit=1234')
    assert response.status_code == 404


def test_should_redirect_to_show_when_create_success(client, monkeypatch):
    monkeypatch.setattr(paste, 'make_id', lambda: 'zyxw')

    with client as c:
        response = c.post('/', data={'text': 'Do you like pancakes?', 'extension': '', 'delete_after': '3'})
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/zyxw'
        assert session.get('created_ids') == ['zyxw']


def test_should_return_plain_text_when_accept_plain_text(client, monkeypatch):
    monkeypatch.setattr(paste, 'make_id', lambda: 'zyxw')

    response = client.post('/', data={'text': 'stuff and things', 'extension': '', 'delete_after': '3'}, headers={'Accept': 'text/plain'})
    assert response.status_code == 200
    assert response.data == b'http://localhost/zyxw'
    assert response.headers['Content-Type'] == 'text/plain'


def test_should_rerender_edit_when_missing_fields(client):
    response = client.post('/')
    assert response.status_code == 200
    assert b'Some text is required.' in response.data


def test_should_rerender_when_delete_field_more_than_7(client):
    response = client.post('/', data={'text': 'Do you like french toast?', 'extension': '', 'delete_after': '8'})
    assert b'Delete after must be from 1 to 7.' in response.data


def test_should_rerender_when_delete_field_less_than_1(client):
    response = client.post('/', data={'text': 'Do you like french toast?', 'extension': '', 'delete_after': '-1'})
    assert b'Delete after must be from 1 to 7.' in response.data
