from django.core.management.base import BaseCommand
from payments.kafka.consumer import listen_to_payment_topic
from payments.kafka.product_consumer import listen_to_product_topic
import threading

class Command(BaseCommand):
    help = "Kafka starting..."

    def handle(self, *args, **options):
        payment_thread = threading.Thread(target=listen_to_payment_topic)
        product_thread = threading.Thread(target=listen_to_product_topic)

        payment_thread.start()
        product_thread.start()

        payment_thread.join()
        product_thread.join()