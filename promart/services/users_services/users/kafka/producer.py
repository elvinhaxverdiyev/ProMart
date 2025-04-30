from kafka import KafkaProducer
import json

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers="kafka:9092", 
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),  
            key_serializer=lambda k: str(k).encode('utf-8')  
        )
    return _producer

def send_message(topic, key, value):
    producer = get_producer()
    producer.send(topic, key=key, value=value)
    producer.flush()
