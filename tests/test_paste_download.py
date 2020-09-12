
def test_should_return_download_txt_when_paste_exists(client, monkeypatch):
    response = client.get('/download/abcd')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=abcd.txt'
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'


def test_should_return_download_with_extension_when_paste_exists(client, monkeypatch):
    response = client.get('/download/abcd.md')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=abcd.md'
    assert response.headers['Content-type'] == 'text/plain; charset=utf-8'


def test_should_return_404_when_paste_does_not_exist(client, monkeypatch):
    response = client.get('/download/1234')
    assert response.status_code == 404
    assert response.headers['Content-type'] == 'text/html; charset=utf-8'
