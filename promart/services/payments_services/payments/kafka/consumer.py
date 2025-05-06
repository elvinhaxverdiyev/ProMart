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
    logger.info(f"Starting Kafka consumer for topic: {settings.KAFKA_PAYMENT_TOPIC}")
    try:
        for message in consumer:
            order_data = message.value
            logger.info(f"Received message from Kafka: {order_data}")
            try:
                process_payment_event(order_data)
            except Exception as e:
                logger.error(f"Error processing payment event: {e}")
    except Exception as e:
        logger.error(f"Kafka consumer error: {e}")
        consumer.close()