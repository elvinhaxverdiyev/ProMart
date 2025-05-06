import json
from kafka import KafkaConsumer
from django.conf import settings
from payments.models.product_cache import ProductCache
import logging

logger = logging.getLogger(__name__)

consumer = KafkaConsumer(
    settings.KAFKA_PRODUCT_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="payment_product_group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

def listen_to_product_topic():
    logger.info(f"Starting Kafka consumer for topic: {settings.KAFKA_PRODUCT_TOPIC}")
    try:
        for message in consumer:
            product_data = message.value
            logger.info(f"Received product data: {product_data}")
            try:
                ProductCache.objects.update_or_create(
                    product_id=product_data["id"],
                    defaults={
                        "name": product_data["name"],
                        "price": product_data["price"]
                    }
                )
                logger.info(f"Product {product_data['id']} cached.")
            except Exception as e:
                logger.error(f"Error caching product: {e}")
    except Exception as e:
        logger.error(f"Kafka consumer error: {e}")
        consumer.close()