import redis
import logging
from django.conf import settings

__all__ = [
    "redis_client"
]

# Configure logging
logger = logging.getLogger(__name__)

"""
Initialize a Redis client using Django settings.

This client can be used across the application to interact with the Redis server,
for purposes such as caching, task queuing, or temporary data storage.
"""

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=settings.REDIS_DB,
        decode_responses=True
    )
    logger.info("Redis client initialized successfully.")
except Exception as e:
    logger.exception(f"Failed to initialize Redis client: {e}")
    redis_client = None
