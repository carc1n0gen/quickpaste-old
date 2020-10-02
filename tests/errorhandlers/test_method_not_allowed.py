

def test_should_respond_405_when_post_to_show_paste_route(client):
    response = client.post('/foobar.txt')
    assert response.status_code == 405
    assert b'You can&#39;t do that here.' in response.data
