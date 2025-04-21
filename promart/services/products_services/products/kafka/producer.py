from kafka import KafkaProducer
from django.conf import settings
import json

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(data):
    producer.send(settings.KAFKA_TOPIC, data)
    producer.flush()