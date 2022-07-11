from copy import deepcopy

from sqlalchemy import TIMESTAMP, VARCHAR, CheckConstraint, Column, Enum, Numeric, Table

from microservices.settings import base_fields, metadata, State

events_model = Table(
    "events",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("title", VARCHAR(length=255), nullable=False, comment="Название"),
    Column("coefficient", Numeric(4, 2), nullable=False, comment="Коэффициент ставки на выигрыш"),
    Column("deadline", TIMESTAMP(timezone=True), nullable=False, comment="Таймстемп, до которого на событие принимаются ставки"),
    Column("state", Enum(State), nullable=False, comment="Текущий статус события"),
    CheckConstraint("coefficient > 0", name="positive_number"),
    schema="line_provider",
    comment="События"
)

__all__ = ["events_model", "metadata"]
