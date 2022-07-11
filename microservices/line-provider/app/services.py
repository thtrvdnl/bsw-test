from typing import Mapping

import ujson
from fastapi import HTTPException
from pydantic import UUID4

from app.models import events_model
from app.serializers import EventCreate, EventPatch
from loguru import logger

from app.utils import get_deadline_seconds
from microservices.settings import database, redis, base_conf


async def create_event(event: EventCreate) -> Mapping:
    event_record = await database.fetch_one(
        events_model.insert().returning(events_model).values(**event.dict())
    )
    await redis.set(
        name=str(event_record["uuid"]),
        value=ujson.dumps(event.dict(exclude={"deadline", "state"})),
        ex=get_deadline_seconds(
            now=event_record["created_at"], deadline=event.deadline
        ),
    )
    logger.info(
        f"Create event {event_record['title']} with deadline {event_record['deadline']} | uuid: {event_record['uuid']}"
    )
    return event_record


async def patch_event(uuid: UUID4, event: EventPatch) -> Mapping:
    query = (
        events_model.update()
        .returning(events_model)
        .values(**event.dict(exclude_unset=True))
        .where(events_model.c.uuid == uuid)
    )
    if event_record := await database.fetch_one(query):
        message = {"uuid": str(event_record["uuid"])} | event.dict(
            include={"state"}, exclude_unset=True
        )
        await redis.publish(
            channel=base_conf.redis_channel_events,
            message=ujson.dumps(message),
        )
        logger.info(f"Update event {event_record['title']}: {message}")
        return event_record

    raise HTTPException(status_code=404, detail="UUID not found")


__all__ = ["create_event", "patch_event"]
