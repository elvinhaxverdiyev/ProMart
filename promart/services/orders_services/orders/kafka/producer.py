# orders/kafka/producer.py

import json
from kafka import KafkaProducer
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_order_to_payment_topic(order_data: dict):
    """
    payment_topic-ə sifariş məlumatını göndərir
    """
    producer.send(settings.KAFKA_PAYMENT_TOPIC, value=order_data)
    producer.flush()
