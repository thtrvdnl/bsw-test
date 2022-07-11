"""create table events

Revision ID: b8b5d50c680c
Revises: 3a285d9ec7d6
Create Date: 2022-07-10 14:03:43.895042

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app import events_model
from microservices.settings import create_datetime_trigger, drop_datetime_trigger

revision = 'b8b5d50c680c'
down_revision = '3a285d9ec7d6'
branch_labels = None
depends_on = None


def upgrade():
    # fmt: off
    op.create_table(
        'events',
        sa.Column('uuid', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False, comment='UUID ресурса'),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Дата создания ресурса'),
        sa.Column('modified_at', postgresql.TIMESTAMP(timezone=True), nullable=False, comment='Дата изменения ресурса'),
        sa.Column('title', sa.VARCHAR(length=255), nullable=False, comment='Название'),
        sa.Column('coefficient', sa.Numeric(precision=4, scale=2), nullable=False, comment='Коэффициент ставки на выигрыш'),
        sa.Column('deadline', sa.TIMESTAMP(timezone=True), nullable=False, comment='Таймстемп, до которого на событие принимаются ставки'),
        sa.Column('state', sa.Enum('new', 'finished_win', 'finished_lose', name='state'), nullable=False, comment='Текущий статус события'),
        sa.CheckConstraint('coefficient > 0', name='positive_number'),
        sa.PrimaryKeyConstraint('uuid'),
        schema='line_provider',
        comment='События'
    )
    create_datetime_trigger(events_model)(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(events_model)(target=None, bind=op.get_bind())
    op.drop_table('events', schema='line_provider')
