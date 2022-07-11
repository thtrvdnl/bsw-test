from copy import deepcopy

from sqlalchemy import CheckConstraint, Column, Enum, Numeric, Table, text
from sqlalchemy.dialects.postgresql import UUID

from microservices.settings import base_fields, metadata, State

bets_model = Table(
    "bets",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("event_uuid", UUID, nullable=False, comment="UUID события"),
    Column("amount", Numeric(scale=2), nullable=False, comment="Сумма ставки"),
    Column("state", Enum(State), server_default=text(f"'{State.new}'"), nullable=False, comment="Текущий статус события"),
    CheckConstraint("amount > 0", name="positive_number"),
    schema="bet_maker",
    comment="Ставки"
)

__all__ = ["bets_model", "metadata", "State"]
