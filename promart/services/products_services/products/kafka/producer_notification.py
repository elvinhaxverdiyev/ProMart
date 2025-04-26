# producer_notification.py
from kafka import KafkaProducer
import json
from django.conf import settings
from products.models import Product

# Kafka producer yaratmaq
producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON formatında məlumatı serialize edirik
)

def send_product_to_notification(product):
    """
    Məhsul yaradıldıqda, məhsul məlumatlarını Notification Service-ə göndərir.
    
    :param product: Yaradılan məhsul obyektinin məlumatları
    """
    product_data = {
        "product_id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "stock": product.stock,
    }

    # Kafka mövzusuna göndəririk
    producer.send(settings.KAFKA_PRODUCT_TOPIC, product_data)
    producer.flush()

    print(f"Product data sent to Notification Service for product: {product.name}")
