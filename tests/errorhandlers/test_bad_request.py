## THESE TESTS DONT DO ANYTHING YET BECAUSE THE APP JUST
## RENDERS THE CREATE PAGE WHEN VALIDATION FAILS


# def test_should_return_html(client, monkeypatch):
#     response = client.post('/')
#     assert response.status_code == 200
#     assert response.headers['Content-type'] == 'text/html; charset=utf-8'

# def test_should_return_plaintext(client, monkeypatch):
#     response = client.post('/', headers={'Accept': 'text/plain'})
#     # print(response.data)
#     assert response.status_code == 400
#     assert response.headers['Content-type'] == 'text/plain; charset=utf-8'