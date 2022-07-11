from sqlalchemy import Column, FetchedValue, MetaData, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from enum import Enum as PyEnum


class State(PyEnum):
    new = "new"
    finished_win = "finished_win"
    finished_lose = "finished_lose"


metadata = MetaData()
base_fields = (
    # fmt: off
    Column("uuid", UUID, primary_key=True, server_default=func.uuid_generate_v4(), comment="UUID ресурса"),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment="Дата создания ресурса"),
    Column("modified_at", TIMESTAMP(timezone=True), server_onupdate=FetchedValue(), nullable=False, comment="Дата изменения ресурса"),
)


__all__ = ["base_fields", "metadata", "State"]
