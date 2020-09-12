import click
import pymongo
from datetime import datetime, timezone
from flask.json import dump, load
from app.repositories import get_db
from app.permanent_pastes import about_text, cli_text


def configure_delete_index():
    db = get_db()
    pastes = db['pastes']

    try:
        pastes.drop_index('paste_ttl')
    except pymongo.errors.OperationFailure:
        pass

    pastes.create_index('delete_at', expireAfterSeconds=0, name='paste_ttl')


def create_or_update_permanent_pastes():
    db = get_db()
    db['pastes'].update_one(
        {'_id': 'about'},
        {'$set': {
            '_id': 'about',
            'text': about_text,
            'created_at': datetime.utcnow(),
            'delete_at': None
        }},
        upsert=True
    )

    db['pastes'].update_one(
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

    @app.cli.command(help='Export the database to json files.')
    @click.option('--output', help='Path to output file.')
    def export_db(output='output.json'):
        db = get_db()
        cursor = db['pastes'].find()

        pastes = [{
            '_id': item['_id'],
            'text': item['text'],
            'created_at': item['created_at'].timestamp(),
            'delete_at': item['delete_at'].timestamp() if item['delete_at'] else None
        } for item in cursor]

        with open(output, 'w') as f:
            dump(pastes, f)
        print(f'Exported database to {output}')

    @app.cli.command(help='Import json files to the database.')
    @click.option('--input', help='Path to input file.')
    def import_db(input='output.json'):
        db = get_db()
        with open(input, 'r') as f:
            pastes = [{
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
            } for paste in load(f)]
            db['pastes'].insert_many(pastes)
        print(f'Imported data from {input}')
