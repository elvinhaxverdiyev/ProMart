from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger(__name__)
_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: str(k).encode("utf-8"),
            retries=5
        )
    return _producer

def send_message(topic, key, value):
    producer = get_producer()
    try:
        producer.send(topic, key=key, value=value)
        producer.flush()
        logger.info(f"Message sent to topic {topic}: {value}")
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")
