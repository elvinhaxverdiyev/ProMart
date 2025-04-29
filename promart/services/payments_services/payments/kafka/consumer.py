import json
from kafka import KafkaConsumer
from django.conf import settings

def start_payment_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_PAYMENT_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='payment-service-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("Payment Kafka Consumer started...")

    for message in consumer:
        data = message.value
        print("Received payment event:", data)
        process_payment_event(data)

def process_payment_event(data):
    # Burada ödəniş məlumatlarını işləyə bilərsən
    user_id = data.get("user_id")
    order_id = data.get("order_id")
    amount = data.get("amount")
    method = data.get("method")

    # Məsələn, Payment modelində ödənişi yarada bilərsən
    from payments.models.payments_models import Payment
    Payment.objects.create(
        user_id=user_id,
        order_id=order_id,
        amount=amount,
        payment_method=method,
        status="pending"  # ya da ilkin status
    )
