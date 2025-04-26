# producer_notification_consumer.py
from kafka import KafkaConsumer
import json
from django.conf import settings
from notifications.models import Notifications

# Kafka consumer yaratmaq
consumer = KafkaConsumer(
    settings.KAFKA_PRODUCT_TOPIC,  # Kafka mövzu adı
    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],  # Kafka server bağlantısı
    auto_offset_reset='earliest',  # İlk mesajdan başlayaraq oxumaq
    enable_auto_commit=True,  # Kafka avtomatik olaraq mesajları qeydə alır
    group_id='product-notification-group',  # Consumer qrup adı
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # JSON formatında məlumatı deserializasiya edirik
)

print("Kafka consumer started for product data. Waiting for messages...")

# Kafka mövzusundan mesajları oxuyuruq
for message in consumer:
    data = message.value  # Kafka mesajının dəyərini əldə edirik
    print("Received product data:", data)

    # Məhsul məlumatları
    product_data = {
        "product_id": data.get("product_id"),
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "stock": data.get("stock"),
    }

    # Notification modelinə məlumatı əlavə edirik
    notification_data = {
        "product": product_data,  # Məhsul məlumatları
        "message": f"Yeni məhsul: {product_data['name']} satışa çıxarıldı!"
    }
    notification = Notifications(**notification_data)
    notification.save()  # Yeni notification-u yadda saxlayırıq

    print(f"Notification created for product: {product_data['name']}")
