import logging

import aioredis
import databases
from loguru import logger
from pydantic import BaseSettings, PostgresDsn, RedisDsn


def configure_logger(service_name: str):
    """Configuring a logger for the entire project."""

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level="NOTSET")
    logger.add(
        sink=f"logs/{service_name}.log",
        level="INFO",
        format="uptime:{elapsed} | time:{time} | {level} | {name}:{line} | {message}",
        rotation="1 month",
        compression="gz",
    )


class BaseConfig(BaseSettings):
    db_url: PostgresDsn
    redis_url: RedisDsn
    redis_channel_events: str = "events"


base_conf = BaseConfig()
database = databases.Database(base_conf.db_url)
redis = aioredis.from_url(base_conf.redis_url, encoding="utf-8")
pubsub = redis.pubsub()

__all__ = ["base_conf", "database", "redis", "configure_logger", "pubsub"]
