import os
import hashlib
import pytest
from alembic import command
from alembic.config import Config

from app import app
from app import limiter

@pytest.fixture
def client():
    app.config['DB_PATH'] = 'database-test.db'
    app.config['TESTING'] = True
    limiter.enabled = False
    config = Config('alembic.ini')
    config.set_main_option('sqlalchemy.url', 'sqlite:///database-test.db')
    command.upgrade(config, 'head')
    client = app.test_client()
    yield client
    os.remove('database-test.db')


def test_should_return_200(client):
    rv = client.get('/')
    assert rv.status == '200 OK'
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_404_html(client):
    rv = client.get('/foobar')
    assert rv.status == '404 NOT FOUND'
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_redirect_to_home(client):
    rv = client.post('/')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == 'http://localhost/'


def test_should_return_400(client):
    rv = client.post('/', headers={'X-Respondwith': 'link'})
    assert rv.status == '400 BAD REQUEST'
    assert rv.headers['Content-type'] == 'text/plain'


def test_should_return_redirect_to_paste(client):
    hash = hashlib.md5(b'hello_world')
    rv = client.post('/', data={'text': 'hello_world'})
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == 'http://localhost/{}'.format(hash.hexdigest())


def test_should_return_link_to_paste(client):
    hash = hashlib.md5(b'hello_world')
    rv = client.post('/', data={'text': 'hello_world'}, headers={'X-Respondwith': 'link'})
    assert rv.status == '200 OK'
    assert rv.headers['Content-type'] == 'text/plain'
