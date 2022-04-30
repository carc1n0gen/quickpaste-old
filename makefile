all: deps assets init-db

deps:
	pipenv sync
	npm ci

assets:
	npm run prod

init-db:
	FLASK_APP=app.create_app pipenv run flask init-db

dev-deps:
	pipenv sync --dev
	npm install

dev-assets:
	npm run development

watch-assets:
	npm run watch

dev-run:
	pipenv run flask run

test:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run pytest

test-coverage:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run pytest --cov

coverage:
	PYTHONPATH=. FLASK_APP=app.create_app pipenv run coverage html