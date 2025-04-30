from django.conf import settings
import requests
import json
import logging
from utils.redis_client import redis_client

__all__ = [
    "is_seller",
]

# Configure logging
logger = logging.getLogger(__name__)

def is_seller(user_id: int) -> bool:
    """
    Check if a user is a seller based on their user ID.

    First, it attempts to retrieve the user type from Redis cache. If not found or invalid, 
    it makes a request to an external user service. If the user type is successfully retrieved, 
    it determines whether the user is a seller.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user is a seller, False otherwise.
    """
    redis_key = f"user:{user_id}"
    logger.debug(f"Checking Redis for user type with key: {redis_key}")
    
    user_json = redis_client.get(redis_key)

    if user_json:
        try:
            user_data = json.loads(user_json)
            is_seller = user_data.get("user_type") == "seller"
            logger.info(f"User type retrieved from Redis: {user_data.get("user_type")}")
            return is_seller
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to decode JSON from Redis for user {user_id}: {e}")

    try:
        url = f"{settings.USER_SERVICE_URL}/users/{user_id}/type"
        logger.debug(f"Requesting user type from external service: {url}")
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            user_type = response.json().get("user_type")
            logger.info(f"User type retrieved from API: {user_type}")
            return user_type == "seller"
        else:
            logger.warning(f"Non-200 response from user service: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Request to user service failed: {e}")

    logger.info(f"User {user_id} is not a seller or information unavailable.")
    return False
