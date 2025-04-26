from django.conf import settings
import requests
import json
from utils.redis_client import redis_client

def is_seller(user_id: int) -> bool:
    """
    Checks if the user with the given user_id is a seller.

    This function first checks if the user type is cached in Redis. If the user type is 
    found in the Redis cache, it returns whether the user is a seller. If not, it makes 
    a request to an external user service to fetch the user type.

    Args:
        user_id (int): The ID of the user whose type is to be checked.

    Returns:
        bool: True if the user is a seller, False otherwise.
    """
    redis_key = f"user:{user_id}"
    user_json = redis_client.get(redis_key)

    if user_json:
        try:
            user_data = json.loads(user_json)
            return user_data.get("user_type") == "seller"
        except json.JSONDecodeError:
            pass

    try:
        url = f"{settings.USER_SERVICE_URL}/users/{user_id}/type"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            user_type = response.json().get("user_type")
            return user_type == "seller"
    except requests.RequestException:
        pass

    return False
