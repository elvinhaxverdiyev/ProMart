import json
import logging
from kafka import KafkaProducer
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_order_to_payment_topic(order_data: dict):
    """
    Sends order data to the payment_topic.
    """
    try:
        producer.send(settings.KAFKA_PAYMENT_TOPIC, value=order_data)
        producer.flush()
        logger.info("Order data sent to Kafka payment topic: %s", order_data)
    except Exception as e:
        logger.error("Failed to send order data to Kafka: %s", e)
