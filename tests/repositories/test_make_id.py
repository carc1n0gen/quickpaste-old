from app.repositories import make_id


def test_should_have_correct_length(app):
    app.config['PASTE_ID_LENGTH'] = 4
    with app.app_context():
        id = make_id()
        assert len(id) == 4
