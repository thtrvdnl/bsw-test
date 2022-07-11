"""create basic functions and extensions

Revision ID: 3a285d9ec7d6
Revises: 
Create Date: 2022-07-10 13:58:12.257229

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from microservices.settings import update_datetime

revision = "3a285d9ec7d6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS line_provider")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute(update_datetime())


def downgrade():
    op.execute("DROP FUNCTION update_datetime()")
    op.execute('DROP EXTENSION "uuid-ossp"')
    op.execute("DROP SCHEMA line_provider CASCADE")
