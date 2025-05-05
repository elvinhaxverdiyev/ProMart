import json
from kafka import KafkaConsumer
from django.conf import settings
from payments.services.paypal_service import process_payment_event
import logging

logger = logging.getLogger(__name__)

consumer = KafkaConsumer(
    settings.KAFKA_PAYMENT_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="order_payment_group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

def listen_to_payment_topic():
    """
    Listens to the Kafka payment topic and processes incoming order data.

    This function continuously consumes messages from the configured Kafka
    payment topic. For each received message, it logs the order data and 
    triggers the payment processing logic via the `process_payment_event` function.
    """
    logger.info(f"Listening to topic: {settings.KAFKA_PAYMENT_TOPIC}")
    for message in consumer:
        order_data = message.value
        logger.info(f"Order data received: {order_data}")
        process_payment_event(order_data)