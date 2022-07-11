from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class Data(BaseModel):
    id: UUID4 | None = Field(title="ID ресурса")
    attributes: list | dict | None = Field(title="Атрибуты ресурса")


class SuccessResponse(BaseModel):
    data: Data | list[Data] | None = Field(title="Данные ресурса")


class Attributes(BaseModel):
    created_at: datetime = Field(..., title="Дата создания ресурса")
    modified_at: datetime = Field(..., title="Дата изменения ресурса")


__all__ = ["SuccessResponse", "Data", "Attributes"]
