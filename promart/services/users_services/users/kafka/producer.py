import json
import time
import logging
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from django.conf import settings
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

# Set up logger
logger = logging.getLogger(__name__)

# Global variable for lazy initialization
_producer = None

def create_kafka_producer(retries=5, delay=3):
    """
    Creates a KafkaProducer instance with retry logic in case the broker is not available.

    :param retries: Number of retry attempts
    :param delay: Delay between retries in seconds
    :return: KafkaProducer instance
    :raises: Exception if broker is unavailable after retries
    """
    for attempt in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka producer created successfully.")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"[Kafka] Broker not available (attempt {attempt + 1}/{retries})... retrying in {delay}s")
            time.sleep(delay)
    logger.error("Kafka broker not available after retries.")
    raise Exception("Kafka broker not available after retries")

def get_kafka_producer():
    """
    Lazily initializes and returns the KafkaProducer instance.
    """
    global _producer
    if _producer is None:
        _producer = create_kafka_producer()
    return _producer

def send_user_data_to_kafka(user_id):
    """
    Sends user data to a Kafka topic based on the given user ID.

    :param user_id: ID of the user to send
    """
    try:
        user = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
        return

    user_data = {
        "user_id": user.id,
        "email": user.email,
        "phone_number": user.phone_number,
        "user_type": user.user_type,
        "profile_picture": user.profile_picture.url if user.profile_picture else None
    }

    try:
        producer = get_kafka_producer()  
        producer.send(settings.KAFKA_TOPIC, user_data)
        producer.flush()
        logger.info(f"Sent user {user.id} data to Kafka topic: {settings.KAFKA_TOPIC}")
    except Exception as e:
        logger.error(f"Failed to send user data to Kafka: {e}")
