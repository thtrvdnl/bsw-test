from app import router
from fastapi import FastAPI

from microservices.settings import configure_logger, database

configure_logger(service_name="line-provider")

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
