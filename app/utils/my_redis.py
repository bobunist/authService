from functools import lru_cache

import redis.asyncio as redis

redis = redis.Redis()


@lru_cache
def get_redis():
    return redis
