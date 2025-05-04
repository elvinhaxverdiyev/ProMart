import json
from kafka import KafkaConsumer
from django.conf import settings
from payments.models.product_cache import ProductCache

consumer = KafkaConsumer(
    "product_topic",  
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="payment_product_group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

def listen_to_product_topic():
    print(f"Listening to topic: product_topic")
    for message in consumer:
        product_data = message.value
        print(f"Product data received from Kafka: {product_data}")
        try:
            ProductCache.objects.update_or_create(
                product_id=product_data["id"],
                defaults={
                    "name": product_data["name"],
                    "price": product_data["price"]
                }
            )
            print(f"Product {product_data['id']} saved.")
        except Exception as e:
            print(f"Error saving product data: {e}")
