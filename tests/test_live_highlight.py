

def test_should_return_400_when_missing_required_fields(client):
    response = client.post('/highlight')
    assert response.status_code == 400


def test_shoudl_return_200_when_required_fields_present(client):
    response = client.post('/highlight', data={'text': 'Honk! I\'m a goose!', 'extension': '', 'delete_after': '3'})
    assert response.status_code == 200
