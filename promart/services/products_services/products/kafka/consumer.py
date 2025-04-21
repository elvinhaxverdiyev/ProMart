from kafka import KafkaConsumer
import json
from django.conf import settings
from users.models import CustomUser

# Kafka consumer yarat
consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='product-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Kafka consumer işə salındı. Mesajlar gözlənilir...")

# Kafka mövzusundan mesajları oxu
for message in consumer:
    data = message.value
    print("Gələn mesaj:", data)

    user_id = data.get("user_id")
    try:
        user = CustomUser.objects.get(id=user_id)
        # İstifadəçi məlumatlarını Kafka mesajına görə yeniləyin
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.user_type = data.get("user_type", user.user_type)
        user.save()
        print(f"İstifadəçi yeniləndi: {user_id}")
    except CustomUser.DoesNotExist:
        print(f"İstifadəçi tapılmadı: {user_id}")
