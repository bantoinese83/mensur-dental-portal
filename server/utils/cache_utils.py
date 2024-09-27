# utils/cache_utils.py
from typing import Optional

from core.redis_config import redis_client


def set_cache(key: str, value: str, expire: Optional[int] = None):
    """
    Set a value in the cache with an optional expiration time.
    """
    redis_client.set(name=key, value=value, ex=expire)


def get_cache(key: str) -> Optional[str]:
    """
    Get a value from the cache.
    """
    return redis_client.get(name=key)


def delete_cache(key: str):
    """
    Delete a value from the cache.
    """
    redis_client.delete(name=key)
