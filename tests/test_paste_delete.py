
def test_should_success_when_id_in_session(client, monkeypatch):
    with client.session_transaction() as sess:
        sess['created_ids'] = ['abcd']

    response = client.post('/abcd/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Paste has been deleted.' in response.data


def test_should_error_when_id_not_in_session(client, monkeypatch):
    response = client.post('/abcd/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'You don&#39;t have permission to delete this paste [abcd].' in response.data


def test_should_404_when_id_in_session_but_not_in_db(client, monkeypatch):
    with client.session_transaction() as sess:
        sess['created_ids'] = ['1234']

    response = client.post('/1234/delete', follow_redirects=True)
    assert response.status_code == 404
    assert b'Not Found' in response.data    
