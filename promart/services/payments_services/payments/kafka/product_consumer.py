import json
import logging
from kafka import KafkaConsumer
from django.conf import settings
from payments.models.product_cache import ProductCache

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Kafka Consumer for product topic
consumer = KafkaConsumer(
    "product_topic",
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="payment_product_group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

def listen_to_payment_topic():
    """
    Listens to the Kafka payment topic and processes incoming order data.

    This function continuously consumes messages from the Kafka topic
    defined in `settings.KAFKA_PAYMENT_TOPIC`, logs the received order data,
    and passes it to the `process_payment_event` function.
    """
    logger.info(f"Listening to topic: {settings.KAFKA_PAYMENT_TOPIC}")
    for message in consumer:
        order_data = message.value
        logger.info(f"Order data received: {order_data}")
        process_payment_event(order_data)

def listen_to_product_topic():
    """
    Listens to the Kafka product topic and updates or creates product cache.

    This function consumes messages from the 'product_topic' Kafka topic,
    deserializes the JSON message, and uses the `ProductCache` model to update
    or create the product entry in the database. Logs are recorded for each action.
    """
    logger.info("Listening to topic: product_topic")
    for message in consumer:
        product_data = message.value
        logger.info(f"Product data received from Kafka: {product_data}")
        try:
            ProductCache.objects.update_or_create(
                product_id=product_data["id"],
                defaults={
                    "name": product_data["name"],
                    "price": product_data["price"]
                }
            )
            logger.info(f"Product {product_data['id']} saved.")
        except Exception as e:
            logger.error(f"Error saving product data: {e}")
