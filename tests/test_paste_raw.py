
def test_should_return_raw_text_when_paste_found(client, monkeypatch):
    response = client.get('/raw/abcd')
    assert response.status_code == 200
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'
    assert response.headers['X-Content-Type-Options'] == 'nosniff'


def test_should_return_404_when_paste_not_found(client, monkeypatch):
    response = client.get('/raw/1234')
    assert response.status_code == 404
    assert response.headers['Content-type'] == 'text/html; charset=utf-8'
