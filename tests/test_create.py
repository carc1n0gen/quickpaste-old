import hashlib
from app import db, limiter


def test_should_return_200(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_redirect_to_home(client):
    rv = client.post('/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/'


def test_should_return_413(client):
    text = 'aaaaaaaaaaaaaaaaaaaaa'
    rv = client.post('/', data={'text': text})
    assert rv.status_code == 413
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_429(client):
    limiter.enabled = True
    client.get('/')
    client.get('/')
    rv = client.get('/')
    assert rv.status_code == 429


def test_should_return_400(client):
    rv = client.post('/', headers={'X-Respondwith': 'link'})
    assert rv.status_code == 400
    assert rv.headers['Content-type'] == 'text/plain; charset=utf-8'


def test_should_return_500(client):
    db.engine.execute('DROP TABLE pastes')
    # Need to do this to reset migrations history
    db.engine.execute('DROP TABLE alembic_version')
    rv = client.post('/', data={'text': 'foo'})
    assert rv.status_code == 500


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
    assert rv.headers['Content-type'] == 'text/plain; charset=utf-8'
