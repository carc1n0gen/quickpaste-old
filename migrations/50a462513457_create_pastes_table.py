"""create pastes table

Revision ID: 50a462513457
Create Date: 2019-01-17 12:10:06.961637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50a462513457'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pastes',
        sa.Column('hash', sa.LargeBinary(16)),
        sa.Column('text', sa.Text()),
        sa.Column('timestamp', sa.TIMESTAMP()),
        sa.PrimaryKeyConstraint('hash')
    )


def downgrade():
    op.drop_table('pastes')
