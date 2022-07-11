import decimal

from pydantic import UUID4, BaseModel, Field, validator

from microservices.settings import (
    Attributes,
    State,
    generate_response_200,
    generate_response_201,
)
from microservices.settings import Data as BaseData
from microservices.settings import SuccessResponse as BaseSuccessResponse


class BetBase(BaseModel):
    event_uuid: UUID4 = Field(..., title="UUID события")
    amount: decimal.Decimal = Field(..., title="Сумма ставки")

    @validator("amount")
    def positive_number_with_two_decimal_places(cls, value):
        if value <= 0 or value.as_tuple().exponent != -2:
            raise ValueError("No positive number with two decimal places")
        return value


class Bet(BetBase, Attributes):
    state: State = Field(..., title="Cтатус события")


class BetCreate(BetBase):
    ...


class Data(BaseData):
    attributes: Bet = Field(title="Атрибуты ресурса")


class SuccessResponse(BaseSuccessResponse):
    data: Data | list[Data] | None = Field(title="Данные ресурса")


response_200 = generate_response_200(model=SuccessResponse)
response_201 = generate_response_201(model=SuccessResponse)
