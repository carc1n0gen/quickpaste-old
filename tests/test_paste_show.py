from app.repositories import paste
from .mocks import mock_get_paste


def test_should_return_200(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/abcd')
    assert response.status_code == 200
    assert b'The cow goes mooooooo.' in response.data
    assert b'will be deleted in' in response.data


def test_should_return_404(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/1234')
    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_should_container_highlighted_class(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/abcd?h=1')
    assert response.status_code == 200
    assert b'highlighted' in response.data


def test_should_not_show_deleted_in_message(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.get('/about')
    assert response.status_code == 200
    assert b'will be deleted in' not in response.data
