from typing import Tuple

from sqlalchemy import DDL, Table, event
from sqlalchemy.sql.ddl import DDLElement

create_trigger_sql = """
    CREATE TRIGGER {} BEFORE INSERT OR UPDATE
    ON {} FOR EACH ROW EXECUTE PROCEDURE {}()
"""
drop_trigger_sql = """
    DROP TRIGGER IF EXISTS {} ON {}
"""


def _create_trigger(model: Table, trigger_name: str, procedure_name: str) -> DDLElement:
    trigger = DDL(
        create_trigger_sql.format(trigger_name, model.fullname, procedure_name)
    ).execute_if(dialect="postgresql")
    event.listen(model, "after_create", trigger)
    return trigger


def _drop_trigger(model: Table, trigger_name: str) -> DDLElement:
    trigger = DDL(drop_trigger_sql.format(trigger_name, model.fullname)).execute_if(
        dialect="postgresql"
    )
    event.listen(model, "before_drop", trigger)
    return trigger


def initialize_triggers(
    trigger_name: str, procedure_name: str
) -> Tuple[DDLElement, DDLElement]:
    return (lambda model: _create_trigger(model, trigger_name, procedure_name)), (
        lambda model: _drop_trigger(model, trigger_name)
    )


create_datetime_trigger, drop_datetime_trigger = initialize_triggers(
    trigger_name="modified_at", procedure_name="update_datetime"
)


__all__ = [
    "create_datetime_trigger",
    "drop_datetime_trigger",
]
