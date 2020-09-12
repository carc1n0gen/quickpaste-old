
def test_should_show_time_left_in_days(client):
    response = client.get('/days')
    assert response.status_code == 200
    assert b'will be deleted in 5 days' in response.data


def test_should_show_time_left_in_hours(client):
    response = client.get('/hours')
    assert response.status_code == 200
    assert b'will be deleted in 3 hours' in response.data


def test_should_show_time_left_within_the_hour(client):
    response = client.get('/sooooon')
    assert response.status_code == 200
    assert b'will be deleted within the hour' in response.data


def test_should_404_when_paste_not_found(client, monkeypatch):
    response = client.get('/1234')
    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_should_contain_highlighted_class_when_h_param_exists(client, monkeypatch):
    response = client.get('/abcd?h=1')
    assert response.status_code == 200
    assert b'highlighted' in response.data


def test_should_not_show_deleted_when_permanent_paste(client, monkeypatch):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'will be deleted in' not in response.data
