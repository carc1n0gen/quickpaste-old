from datetime import datetime, timedelta
import click
from app.repositories import db


def cleanup_factory(app):
    @click.command(help='Cleanup old pastes')
    def cleanup():
        # Reminder: the timestamp < ? looks backwards because we are storing
        # unix timestamps which are the number of seconds since the epoch.
        # This means that a lower number of seconds is longer ago than a
        # greater number.
        with app.app_context():
            week_ago = datetime.now() - timedelta(weeks=1)
            db.engine.execute(
                'DELETE FROM pastes WHERE timestamp < ?',
                [week_ago.timestamp()]
            )
            print('Deleted pastes older than one week.')

    return cleanup
