import click
from datetime import datetime, timezone
from flask.json import dump, load
from app.repositories import get_db


def create_cli(app):
    @app.cli.command(help='Export the database to json files.')
    @click.option('--output', help='Path to output file.')
    def export_db(output):
        db = get_db()
        cursor = db['pastes'].find()

        pastes = [{
            '_id': item['_id'],
            'text': item['text'],
            'created_at': item['created_at'].timestamp(),
            'delete_at': item['delete_at'].timestamp()
        } for item in cursor]

        with open(output, 'w') as f:
            dump(pastes, f)

    @app.cli.command(help='Import json files to the database.')
    @click.option('--input', help='Path to input file.')
    def import_db(input):
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
                )
            } for paste in load(f)]
            db['pastes'].insert_many(pastes)
