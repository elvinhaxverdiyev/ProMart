from kafka import KafkaProducer
from django.conf import settings
import json

# Create a Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,  # Kafka server connection settings
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages to JSON format
)

def send_message(data):
    """
    Sends a message to the Kafka topic.

    Args:
        data (dict): The data to be sent to the Kafka topic. This should be a dictionary.
    """
    # Send the data to the Kafka topic specified in settings
    producer.send(settings.KAFKA_TOPIC, data)
    
    # Ensure that the message is sent immediately
    producer.flush()
