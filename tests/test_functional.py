import os
import hashlib
import pytest
from app import app, limiter, alembic


@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    limiter.enabled = False
    with app.app_context():
        alembic.upgrade('head')
    client = app.test_client()
    yield client


def test_should_return_200(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_paste_200(client):
    text = 'foobar'
    hash = hashlib.md5(text.encode('utf-8'))
    client.post('/', data={'text': text})
    rv = client.get('http://localhost/{}'.format(hash.hexdigest()))
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_404_html(client):
    rv = client.get('/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_404_html(client):
    rv = client.get('/raw/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_200(client):
    text = 'Hello world'
    hash = hashlib.md5(text.encode('utf-8'))
    client.post('/', data={'text': text})
    rv = client.get('http://localhost/raw/{}'.format(hash.hexdigest()))
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/plain'
    assert rv.data == text.encode('utf-8')


def test_should_return_redirect_to_home(client):
    rv = client.post('/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/'


def test_should_return_400(client):
    rv = client.post('/', headers={'X-Respondwith': 'link'})
    assert rv.status_code == 400
    assert rv.headers['Content-type'] == 'text/plain'


def test_should_return_redirect_to_paste(client):
    hash = hashlib.md5(b'hello_world')
    rv = client.post('/', data={'text': 'hello_world'})
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/{}'.format(
        hash.hexdigest())


def test_should_return_link_to_paste(client):
    rv = client.post('/', data={'text': 'hello_world'},
                     headers={'X-Respondwith': 'link'})
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/plain'
