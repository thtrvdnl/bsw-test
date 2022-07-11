from fastapi import Body, Path
from pydantic import UUID4

from app.serializers import Data, EventCreate, SuccessResponse, Event, EventPatch
from app.services import create_event, patch_event


class EventView:
    @staticmethod
    async def post(event: EventCreate) -> SuccessResponse:
        resource = await create_event(event)
        data = Data(id=resource["uuid"], attributes=Event(**resource))
        return SuccessResponse(data=data)

    @staticmethod
    async def patch(
        uuid: UUID4 = Path(..., alias="id"), event: EventPatch = Body(...)
    ) -> SuccessResponse:
        resource = await patch_event(uuid, event)
        data = Data(id=resource["uuid"], attributes=Event(**resource))
        return SuccessResponse(data=data)

    @staticmethod
    async def delete():
        ...


event_view = EventView
__all__ = ["event_view"]
