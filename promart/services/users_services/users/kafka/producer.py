from kafka import KafkaProducer
import json

_producer = None

def get_producer():
    """
    Returns a singleton KafkaProducer instance.

    If a KafkaProducer does not already exist, it initializes one with the
    specified configuration:
    - `bootstrap_servers`: The Kafka server address.
    - `value_serializer`: Serializes Python objects to JSON-encoded UTF-8.
    - `key_serializer`: Serializes keys as UTF-8 strings.

    Returns:
        KafkaProducer: A singleton KafkaProducer instance.
    """
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers="kafka:9092", 
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),  
            key_serializer=lambda k: str(k).encode('utf-8')  
        )
    return _producer

def send_message(topic, key, value):
    """
    Sends a message to the specified Kafka topic.

    Args:
        topic (str): The name of the Kafka topic.
        key (str or int): The message key used for partitioning.
        value (dict): The message payload to send (will be serialized as JSON).
    
    This function uses the singleton KafkaProducer to send the message and
    then immediately flushes the producer to ensure delivery.
    """
    producer = get_producer()
    producer.send(topic, key=key, value=value)
    producer.flush()
