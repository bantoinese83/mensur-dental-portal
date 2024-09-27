# core/redis_config.py
import os

import redis
from pydantic.v1 import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_DB: int = os.getenv("REDIS_DB", 0)

    class Config:
        env_file = ".env"


redis_settings = RedisSettings()

# Create the Redis client
redis_client = redis.StrictRedis(
    host=redis_settings.REDIS_HOST,
    port=redis_settings.REDIS_PORT,
    db=redis_settings.REDIS_DB,
    decode_responses=True,
)


def init_redis():
    """
    Initialize the Redis client.
    """
    redis_client.ping()
    print("Connected to Redis")
