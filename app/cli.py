import click
import pymongo
from datetime import datetime, timezone
from flask.json import dumps, loads
from app.repositories import database
from app.permanent_pastes import about_text, cli_text


def configure_delete_index():
    pastes = database['pastes']

    try:
        pastes.drop_index('paste_ttl')
    except pymongo.errors.OperationFailure:
        pass

    pastes.create_index('delete_at', expireAfterSeconds=0, name='paste_ttl')


def create_or_update_permanent_pastes():
    database['pastes'].update_one(
        {'_id': 'about'},
        {'$set': {
            '_id': 'about',
            'text': about_text,
            'created_at': datetime.utcnow(),
            'delete_at': None
        }},
        upsert=True
    )

    database['pastes'].update_one(
        {'_id': 'cli'},
        {'$set': {
            '_id': 'cli',
            'text': cli_text,
            'created_at': datetime.utcnow(),
            'delete_at': None
        }},
        upsert=True
    )


def create_cli(app):
    @app.cli.command(help='Initialize or update system db settings.')
    def init_db():
        configure_delete_index()
        create_or_update_permanent_pastes()
        print('Database successfully initialized.')

    @app.cli.command(help='Dump the database as json lines to stdout.')
    def export_db():
        cursor = database['pastes'].find()
        for item in cursor:
            print(dumps({
                '_id': item['_id'],
                'text': item['text'],
                'created_at': item['created_at'].timestamp(),
                'delete_at': item['delete_at'].timestamp() if item['delete_at'] else None
            }))

    @app.cli.command(help='Read json lines from stdin.')
    def import_db():
        stdin = click.get_text_stream('stdin')
        while line := stdin.readline():
            paste = loads(line)
            database['pastes'].insert_one({
                '_id': paste['_id'],
                'text': paste['text'],
                'created_at': datetime.fromtimestamp(
                    paste['created_at'],
                    tz=timezone.utc
                ),
                'delete_at': datetime.fromtimestamp(
                    paste['delete_at'],
                    tz=timezone.utc
                ) if paste['delete_at'] else None
            })
