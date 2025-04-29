from kafka import KafkaConsumer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_PRODUCT_TOPIC = os.getenv("KAFKA_PRODUCT_TOPIC", "products_topic")

consumer = KafkaConsumer(
    KAFKA_PRODUCT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-service-group'
)

def listen_to_products():
    print("Order service Kafka consumer started...")
    for message in consumer:
        product_data = message.value
        print("Yeni məhsul gəldi:", product_data)
        
        # Burda artıq məhsulun id, name və s. var
        product_id = product_data["id"]

        # Burda sən istədiyin kimi `order` və ya `cart` modelinə əlavə edə bilərsən
        # Məsələn, avtomatik məhsulu 'kataloq' siyahısına əlavə etmək və s.
