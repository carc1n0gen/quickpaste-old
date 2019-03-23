import hashlib
import pytest
from datetime import datetime, timedelta
from app import app, limiter, alembic, db, cleanup


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


def test_about_should_return_200(client):
    rv = client.get('/about')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


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


def test_should_return_404_with_valid_hash(client):
    rv = client.get('/00000000000000000000000000000000')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_404_html(client):
    rv = client.get('/raw/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_404_with_valid_hash(client):
    rv = client.get('/raw/00000000000000000000000000000000')
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
    assert rv.headers['Content-type'] == 'text/plain'


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
    assert rv.headers['Content-type'] == 'text/plain'


def test_should_cleanup_old_pastes(client):
    text = 'foo'
    hash = hashlib.md5(text.encode('utf-8'))
    week_ago_and_one_day = datetime.now() - timedelta(weeks=1, days=1)
    db.engine.execute("INSERT INTO pastes VALUES (?, ?, ?)",
                      [hash.digest(), text, week_ago_and_one_day.timestamp()])

    runner = app.test_cli_runner()
    runner.invoke(cleanup)

    result = db.engine.execute('SELECT count(timestamp) FROM pastes')
    assert result.scalar() == 0
