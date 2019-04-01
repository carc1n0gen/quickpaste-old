Quickpaste
==========

A dead simple code snippet sharing tool.

Requirements
------------

* [pipenv](https://pipenv.readthedocs.io/en/latest/) is used for dependency management.

* A database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/latest/core/engines.html#supported-databases)


Setup
-----

1.
	Clone the repo somewhere.  Master *should* always be stable but you can
	checkout the latest tag from [releases](https://github.com/carc1n0gen/quickpaste/releases) if you wish.

	`git clone https://github.com/carc1n0gen/quickpaste.git`

    (optional) `cd quickpaste && git checkout <version>`

2.
	Install dependencies.

	`pipenv sync`

3.
	Run database migrations.

	`pipenv run flask db upgrade head`

Configuration
-------------

Copy the `config.json.example` file to `config.json` in the same directory, and
edit as needed.  Below is a copy of the latest example config.

```json
{
    "BEHIND_PROXY": false,

    "LOG_FILE": "./data/app.log",
    "LOG_LEVEL": "INFO",

    "MAX_PASTE_LENGTH": 10240,
    "MINIFY_PAGE": true,
    "RATELIMIT_DEFAULT": "2 per second",

    "GA_ENABLED": false,
    "GA_ID": "ENTER YOUR GOOGLE ANALYTICS ID",

    "SQLALCHEMY_DATABASE_URI": "sqlite:///data/database.db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": false,

    "MAIL_SERVER": "smtp.example.com",
    "MAIL_PORT": 25,
    "MAIL_USE_TLS": false,
    "MAIL_USE_SSL": false,
    "MAIL_USERNAME": "username",
    "MAIL_PASSWORD": "password",
    "MAIL_DEFAULT_SENDER": "sender <sender@example.com>",
    "MAIL_RECIPIENT": "recipient@example.com"
}
``` 

Updating
--------

Pull the latest changes from master, or checkout the latest tag, sync
dependencies, check for new configuration keys, and run migrations

Running Cleanup
---------------

There is a built in cleanup command to delete pastes that are older than one
week.

`pipenv run flask cleanup`

You will need to configure something like a cron to run that.

Random Things
-------------

**How long are pastes on official [quickpaste](https://quickpaste.net/) kept?**

The built in script that deletes week old pastes is only run once a day.  
there is a window of period where week old pastes stick around, but it isn't
very long.

**Why do I need to configure an email sender?**

If an unknown error occurs in the system, an email containing details will be
sent to the `MAIL_RECIPIENT` configured email.  These details will be vital
for debugging and reporting issues.
