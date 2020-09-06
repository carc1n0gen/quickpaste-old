from app.repositories import paste
from .mocks import mock_get_paste


def test_should_return_200(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/raw/abcd')
    assert response.status_code == 200
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'
    assert response.headers['X-Content-Type-Options'] == 'nosniff'


def test_should_return_404(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/raw/1234')
    assert response.status_code == 404
    assert response.headers['Content-type'] == 'text/html; charset=utf-8'
