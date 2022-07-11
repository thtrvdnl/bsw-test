"""create table bets

Revision ID: e757c42a7f09
Revises: 44a44934109a
Create Date: 2022-07-10 18:14:58.965401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app import bets_model
from microservices.settings import create_datetime_trigger, drop_datetime_trigger

revision = 'e757c42a7f09'
down_revision = '44a44934109a'
branch_labels = None
depends_on = None


def upgrade():
    # fmt: off
    op.create_table(
        'bets',
        sa.Column('uuid', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False, comment='UUID ресурса'),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Дата создания ресурса'),
        sa.Column('modified_at', postgresql.TIMESTAMP(timezone=True), nullable=False, comment='Дата изменения ресурса'),
        sa.Column('event_uuid', postgresql.UUID(), nullable=False, comment='UUID события'),
        sa.Column('amount', sa.Numeric(scale=2), nullable=False, comment='Сумма ставки'),
        sa.Column('state', sa.Enum('new', 'finished_win', 'finished_lose', name='state'), server_default=sa.text("'new'"), nullable=False, comment='Текущий статус события'),
        sa.CheckConstraint('amount > 0', name='positive_number'),
        sa.PrimaryKeyConstraint('uuid'),
        schema='bet_maker',
        comment='Ставки'
    )
    create_datetime_trigger(bets_model)(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(bets_model)(target=None, bind=op.get_bind())
    op.drop_table('bets', schema='bet_maker')

