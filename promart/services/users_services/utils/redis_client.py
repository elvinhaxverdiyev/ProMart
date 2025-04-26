import redis
from django.conf import settings

# Creating a Redis client instance to interact with the Redis database.
redis_client = redis.Redis(
    host=settings.REDIS_HOST,  # The host where the Redis server is located, configured in Django settings.
    port=int(settings.REDIS_PORT),  # The port number for the Redis server, cast to an integer from settings.
    db=settings.REDIS_DB,  # The database index for Redis, configured in Django settings.
    decode_responses=True  # Ensures that the responses from Redis are decoded into strings (instead of bytes).
)
