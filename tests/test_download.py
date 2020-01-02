from app.create_app import shortlink


def test_should_return_404_html(client):
    rv = client.get('/download/foobar')
    assert rv.status_code == 404
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'


def test_should_return_200_with_attachment(client):
    text = 'wow there bud'
    id = shortlink.encode(1)
    client.post('/', data={'text': text})
    rv = client.get(f'/download/{id}')
    assert rv.status_code == 200
    assert rv.headers.get('Content-Disposition') == \
        f'attachment; filename={id}.txt'
