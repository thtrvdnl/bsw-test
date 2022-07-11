import asyncio

from app import router
from fastapi import FastAPI

from app.services import events_reader
from microservices.settings import database, configure_logger, base_conf, pubsub

configure_logger(service_name="bet-maker")

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.include_router(router=router)
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


asyncio.create_task(events_reader(channel=pubsub))
