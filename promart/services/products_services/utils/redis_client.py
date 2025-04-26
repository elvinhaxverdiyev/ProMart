import redis
from django.conf import settings

# Create a Redis client to interact with the Redis server
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    db=settings.REDIS_DB,
    decode_responses=True
)
"""
This creates a Redis client that will connect to a Redis server specified by the Django settings.
The client is configured to decode responses as strings instead of bytes.

Configuration Parameters:
- host (str): The Redis server host, taken from Django settings (REDIS_HOST).
- port (int): The port on which Redis server is running, taken from Django settings (REDIS_PORT).
- db (int): The Redis database number, taken from Django settings (REDIS_DB).
- decode_responses (bool): Set to True to decode Redis responses into strings.

This Redis client will be used for caching and other Redis operations.
"""
