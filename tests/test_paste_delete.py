from app.repositories import paste
from .mocks import mock_get_paste, mock_delete_paste


def test_should_redirect_success_message(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)
    monkeypatch.setattr(paste, 'delete_paste', mock_delete_paste)

    with client.session_transaction() as sess:
        sess['created_ids'] = ['abcd']

    response = client.post('/abcd/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Paste has been deleted.' in response.data


def test_should_redirect_error_message(client, monkeypatch):
    monkeypatch.setattr(paste, 'get_paste', mock_get_paste)

    response = client.post('/abcd/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'You don&#39;t have permission to delete this paste [abcd].' in response.data


def test_should_return_404(client, monkeypatch):
    monkeypatch.setattr(paste, 'delete_paste', mock_delete_paste)

    with client.session_transaction() as sess:
        sess['created_ids'] = ['1234']

    response = client.post('/1234/delete', follow_redirects=True)
    assert response.status_code == 404
    assert b'Not Found' in response.data
