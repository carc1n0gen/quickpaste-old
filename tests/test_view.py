import hashlib


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
    assert rv.headers['Content-type'] == 'text/plain; charset=utf-8'
    assert rv.data == text.encode('utf-8')

