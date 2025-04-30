from kafka import KafkaProducer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC", "users_topic")

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: str(k).encode("utf-8")
        )
    return _producer

def send_user(user_id, user_data):
    """
    Sends user data to the Kafka topic "users_topic".

    Args:
        user_id: The user's ID (used as the message key)
        user_data: A dictionary containing user information
    """
    producer = get_producer()
    producer.send(KAFKA_USER_TOPIC, key=str(user_id), value=user_data)
    producer.flush()
    print(f"User data sent to Kafka: {user_data}")
