import hashlib


def test_should_return_404_html(client):
    rv = client.get('/download/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_404_with_valid_hash(client):
    rv = client.get('/download/00000000000000000000000000000000')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_200_with_attachment(client):
    text = b'hello_world'
    hash = hashlib.md5(text)
    client.post('/', data={'text': text})
    rv = client.get(f'/download/{hash.hexdigest()}')
    assert rv.headers.get('Content-Disposition') == \
        f'attachment; filename={hash.hexdigest()}.txt'
    assert rv.data == text
