def test_about_should_return_200(client):
    rv = client.get('/about')
    assert rv.status_code == 200
    assert rv.headers['Content-type'] == 'text/html; charset=utf-8'
