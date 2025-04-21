from django.conf import settings
import requests
from utils.redis_client import redis_client

def is_seller(user_id: int) -> bool:
    redis_key = f"user:{user_id}"
    user_data = redis_client.hgetall(redis_key)

    if user_data:
        return user_data.get(b"user_type", b"").decode() == "seller"

    try:
        url = f"{settings.USER_SERVICE_URL}/users/{user_id}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            user_type = response.json().get("user_type")
            return user_type == "seller"
    except requests.RequestException:
        pass

    return False
