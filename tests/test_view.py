from app.create_app import shortlink


def test_should_return_paste_200(client):
    text = 'foobar'
    id = shortlink.encode(1)
    client.post('/', data={'text': text})
    rv = client.get(f'/{id}')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_200(client):
    text = 'Hello world'
    id = shortlink.encode(1)
    client.post('/', data={'text': text})
    rv = client.get(f'/raw/{id}')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/plain; charset=utf-8'
    assert rv.data == text.encode('utf-8')


def test_should_return_404_html(client):
    rv = client.get('/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_raw_should_return_404_html(client):
    rv = client.get('/raw/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'
