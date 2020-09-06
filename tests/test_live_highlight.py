

def test_should_return_400(client):
    response = client.post('/highlight')
    assert response.status_code == 400


def test_shoudl_return_200(client):
    response = client.post('/highlight', data={'text': 'Honk! I\'m a goose!', 'extension': ''})
    assert response.status_code == 200
