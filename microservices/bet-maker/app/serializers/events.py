import decimal

from pydantic import Field, BaseModel, UUID4


class Event(BaseModel):
    id: UUID4 = Field(..., title="ID ресурса")
    title: str = Field(..., title="Название", max_length=255)
    coefficient: decimal.Decimal = Field(..., title="Коэффициент ставки на выигрыш")
