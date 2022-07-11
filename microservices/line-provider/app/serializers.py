import decimal
from datetime import datetime

from pydantic import Field, BaseModel, validator, UUID4

from app.models import State
from microservices.settings import Attributes
from microservices.settings import Data as BaseData
from microservices.settings import SuccessResponse as BaseSuccessResponse


class EventBase(BaseModel):
    title: str = Field(..., title="Название", max_length=255)
    coefficient: decimal.Decimal = Field(..., title="Коэффициент ставки на выигрыш")
    state: State = Field(..., title="Cтатус события")
    deadline: datetime = Field(
        None, title="Таймстемп, до которого на событие принимаются ставки"
    )

    @validator("coefficient")
    def positive_number_with_two_decimal_places(cls, value):
        if value <= 0 or value.as_tuple().exponent != -2:
            raise ValueError("No positive number with two decimal places")
        return value


class EventCreate(EventBase):
    deadline: datetime = Field(
        ..., title="Таймстемп, до которого на событие принимаются ставки"
    )
    state: State = Field(State.new, title="Cтатус события")


class EventPatch(EventBase):
    title: str = Field(None, title="Название", max_length=255)
    coefficient: decimal.Decimal = Field(None, title="Коэффициент ставки на выигрыш")
    state: State = Field(None, title="Cтатус события")

    class Config:
        use_enum_values = True


class EventPublish(EventPatch):
    uuid: UUID4 = Field(..., title="ID ресурса")


class Event(EventBase, Attributes):
    ...


class Data(BaseData):
    attributes: Event = Field(title="Атрибуты ресурса")


class SuccessResponse(BaseSuccessResponse):
    data: Data | list[Data] | None = Field(title="Данные ресурса")


__all__ = [
    "Event",
    "EventCreate",
    "EventPatch",
    "EventPublish",
    "Data",
    "SuccessResponse",
]
