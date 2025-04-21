from kafka import KafkaProducer
import json
from django.conf import settings
from users.models import CustomUser
from kafka.errors import NoBrokersAvailable
import time

# Kafka producer-i bir dəfə yaratmaq üçün funksiyanı dəyişdiririk
def create_kafka_producer(retries=5, delay=3):
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,  # settings-dən Kafka ünvanını alırıq
                value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serializasiya
            )
            return producer
        except NoBrokersAvailable:
            print(f"[Kafka] Broker not available (attempt {i+1}/{retries})... retrying in {delay}s")
            time.sleep(delay)
    raise Exception("Kafka broker not available after retries")

# Kafka producer-i yaratmaq
producer = create_kafka_producer()

def send_user_data_to_kafka(user_id):
    """
    Verilən istifadəçi ID-sinə əsaslanaraq Kafka-ya istifadəçi məlumatlarını göndərir.
    """

    # İstifadəçi məlumatlarını əldə etmək
    user = CustomUser.objects.get(id=user_id)
    
    # İstifadəçi məlumatlarını Kafka mesaj formatına uyğunlaşdırmaq
    user_data = {
        "user_id": user.id,
        "email": user.email,
        "phone_number": user.phone_number,
        "user_type": user.user_type,
        "profile_picture": user.profile_picture.url if user.profile_picture else None
    }
    
    # Kafka mövzusuna istifadəçi məlumatlarını göndərmək
    producer.send(settings.KAFKA_TOPIC, user_data)
    producer.flush()
    print(f"Sent user {user.id} data to Kafka")
