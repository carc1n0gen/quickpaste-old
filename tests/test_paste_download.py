
def test_should_return_200(client, monkeypatch):
    response = client.get('/download/abcd')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=abcd.txt'
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'


def test_should_return_200_extension(client, monkeypatch):
    response = client.get('/download/abcd.md')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=abcd.md'
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'


def test_should_return_404(client, monkeypatch):
    response = client.get('/download/1234')
    assert response.status_code == 404
    assert response.headers['Content-type'] == 'text/html; charset=utf-8'
