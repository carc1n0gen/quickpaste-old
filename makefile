dev:
	pipenv run flask run

test:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run pytest

test-coverage:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run pytest --cov

coverage:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run coverage html