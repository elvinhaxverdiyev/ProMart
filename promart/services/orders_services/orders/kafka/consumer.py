import logging
from kafka import KafkaConsumer
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables with defaults
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_PRODUCT_TOPIC = os.getenv("KAFKA_PRODUCT_TOPIC", "products_topic")

# Create Kafka consumer
consumer = KafkaConsumer(
    KAFKA_PRODUCT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="order-service-group"
)

def listen_to_products():
    logger.info("Order service Kafka consumer started...")
    for message in consumer:
        product_data = message.value
        logger.info("New product received: %s", product_data)

        product_id = product_data.get("id")
        product_name = product_data.get("name")
        product_price = product_data.get("price")

        logger.info("Product ID: %s, Name: %s, Price: %s", product_id, product_name, product_price)
