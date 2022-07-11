"""create basic functions and extensions

Revision ID: 44a44934109a
Revises: 
Create Date: 2022-07-10 18:11:52.555300

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from microservices.settings import update_datetime

revision = "44a44934109a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS bet_maker")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute(update_datetime())


def downgrade():
    op.execute("DROP FUNCTION update_datetime()")
    op.execute('DROP EXTENSION "uuid-ossp"')
    op.execute("DROP SCHEMA bet_maker CASCADE")
