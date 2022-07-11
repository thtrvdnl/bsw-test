import asyncio
from typing import Mapping
from uuid import UUID

import aioredis
import async_timeout
import ujson
from fastapi import HTTPException
from fastapi_pagination import paginate

from app.models import bets_model
from app.serializers.bets import BetCreate
from microservices.settings import redis, database, pubsub, base_conf
from loguru import logger


async def create_bet(bet: BetCreate) -> Mapping:
    query = bets_model.insert().returning(bets_model).values(**bet.dict())
    if bet := await database.fetch_one(query=query):
        if await redis.exists(str(bet["event_uuid"])):
            return bet
    raise HTTPException(status_code=404, detail="Event not found")


async def get_bets() -> Mapping:
    if resources := await database.fetch_all(bets_model.select()):
        return resources
    raise HTTPException(status_code=404, detail="Bets not found")


async def get_events() -> list[dict]:
    events_keys = await redis.keys()
    events = [
        {"id": UUID(key.decode("UTF-8"))} | ujson.loads(await redis.get(key))
        for key in events_keys
    ]
    return events


async def events_reader(channel: aioredis.client.PubSub):
    await pubsub.subscribe(base_conf.redis_channel_events)
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    logger.info(f"(Reader) Message Received: {message}")
                    record = ujson.loads(message["data"])
                    resource = await database.fetch_one(
                        bets_model.update()
                        .returning(bets_model)
                        .values(state=record["state"])
                        .where(bets_model.c.event_uuid == record["uuid"])
                    )
                    logger.info(f"Update record: {resource}")
                    if message["data"].decode() == "STOP":
                        logger.info("(Reader) STOP")
                        break
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


__all__ = ["create_bet", "get_bets", "get_events", "events_reader"]
