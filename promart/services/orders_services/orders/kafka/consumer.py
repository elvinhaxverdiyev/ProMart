from kafka import KafkaConsumer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_PRODUCT_TOPIC = os.getenv("KAFKA_PRODUCT_TOPIC", "products_topic")

consumer = KafkaConsumer(
    KAFKA_PRODUCT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="order-service-group"
)

def listen_to_products():
    print("Order service Kafka consumer started...")
    for message in consumer:
        product_data = message.value
        print("Yeni məhsul gəldi:", product_data)

        product_id = product_data.get("id")
        product_name = product_data.get("name")
        product_price = product_data.get("price")

        print(f"Product ID: {product_id}, Name: {product_name}, Price: {product_price}")


