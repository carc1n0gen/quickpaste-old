"""add_id_column

Revision ID: fe792b726385
Create Date: 2019-10-30 15:49:32.285420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe792b726385'
down_revision = '50a462513457'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pastes_new',
        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            autoincrement='auto',
            nullable=False
        ),
        sa.Column('hash', sa.LargeBinary(16)),
        sa.Column('text', sa.Text()),
        sa.Column('timestamp', sa.TIMESTAMP()),
        sa.UniqueConstraint('hash')
    )
    op.execute('''
        INSERT INTO pastes_new (hash, text, timestamp)
        SELECT hash, text, timestamp FROM pastes
    ''')
    op.execute('ALTER TABLE pastes RENAME TO pastes_old')
    op.execute('ALTER TABLE pastes_new RENAME TO pastes')


def downgrade():
    # TODO: Proper down migration.  This could be complicated
    op.drop_column('pastes', 'id')
