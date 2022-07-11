from fastapi import HTTPException, Depends
from fastapi_pagination import paginate, Params

from app.serializers.events import Event
from app.services import get_events
from loguru import logger


class EventView:
    @staticmethod
    async def get(params: Params = Depends()):
        if resources := await get_events():
            events = [Event(**resource) for resource in resources]
            return paginate(events, params)

        raise HTTPException(status_code=404, detail="Events not found")


event_view = EventView
__all__ = ["event_view"]
