Quickpaste
==========

A dead simple code snippet sharing tool.

Requirements
------------

* python 3.9 (_May work on earlier versions but is totally untested_)
* [pipenv](https://pipenv.readthedocs.io/en/latest/) is used for dependency and venv management
* MongoDB


Setup
-----

1.
	Clone the repo somewhere.  Stable *should* always be stable but you can
	checkout the latest tag from [releases](https://github.com/carc1n0gen/quickpaste/releases) if you wish. (Note: the default branch is `develop`, so make sure you switch to `stable`)

	`git clone https://github.com/carc1n0gen/quickpaste.git`

    (optional) `cd quickpaste && git checkout <version>`

2.
    Create a `quickpaste/data` directory.

3.
	Install dependencies.

	`pipenv sync`

    `npm install`

4.
	Initialize the database.

	`pipenv run flask init-db`

5.
    Compile css/js/assets

    `npm run prod`

6.
    Run

    `pipenv run flask run`

Configuration
-------------

Copy the `config.json.example` file to `config.json` in the same directory, and
edit as needed.  Below is a copy of the latest example config. 

*Remember to change the SECRET_KEY!*

```json
{
    "SECRET_KEY": "change me",
    "BEHIND_PROXY": false,

    "LOG_FILE": "./data/app.log",
    "LOG_LEVEL": "INFO",

    "MAX_PASTE_LENGTH": 10240,
    "MINIFY_HTML": true,
    "RATELIMIT_DEFAULT": "2 per second",
    "LINK_ALPHABET": "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-",
    "PASTE_ID_LENGTH": 7,
    "PASTE_EXPIRE_AFTER_SECONDS": 604800,
    "RICH_EDITOR_ENABLED": false,

    "GA_ENABLED": false,
    "GA_ID": "ENTER YOUR GOOGLE ANALYTICS ID",

    "MAIL_SERVER": "smtp.example.com",
    "MAIL_PORT": 25,
    "MAIL_USE_TLS": false,
    "MAIL_USE_SSL": false,
    "MAIL_USERNAME": "username",
    "MAIL_PASSWORD": "password",
    "MAIL_DEFAULT_SENDER": "sender <sender@example.com>",
    "MAIL_RECIPIENT": "recipient@example.com",

    "MONGO_HOST": "127.0.0.1",
    "MONGO_PORT": 27017,
    "MONGO_DATABASE": "quickpaste"
}
``` 

Running In Development
----------------------

`FLASK_ENV=development pipenv run flask run`

If you're making css/js changes, you'll want to watch for changes

`npm run watch`

Running In Production
---------------------

Use a proper wsgi container.  I like to use waitress with nginx reverse proxy
in front of it, but that's totally personal preference.  More info at the
official [flask deployment page](https://flask.palletsprojects.com/en/1.1.x/deploying/).

**Example running with waitress-serve**:

`PYTHONPATH=/path/to/quickpaste waitress-serve --port=8001 --call app.create_app:create_app`

You'll want to configure a daemon of some kind to keep the app running.

Updating
--------

Pull the latest changes from stable, or checkout the latest tag, sync
dependencies, check for new configuration keys, and compile js/css.

1. `git fetch`

2. `git pull` or `git checkout <version>`

3. `pipenv sync`

4. `pipenv run flask init-db`

5. `npm install && npm run prod`

6. restart the app

Contributing
------------

The `stable` branch is like the "master" branch, but pull request should not be made against `stable`.  Make pull requests against the `develop` branch.  I merge `develop` in to `stable` as I see fit.

CLI
---

There are a few cli commands used for administrating a quickpaste instance

`flask init-db` - For creating/updating indexes and permanent pastes

`flask export-db` - Dumps the database as json lines to stdout

`flask import-db` - Imports json lines from stdin to the database

Random Things
-------------

**Why do I need to configure an email sender?**

If an unknown error occurs in the system, an email containing details will be
sent to the `MAIL_RECIPIENT` configured email.  These details will be vital
for debugging and reporting issues.
