from django.core.management.base import BaseCommand
from payments.kafka.consumer import listen_to_payment_topic
from payments.kafka.product_consumer import listen_to_product_topic
from threading import Thread


class Command(BaseCommand):
    help = "Runs Kafka consumers for payment and product topics"

    def handle(self, *args, **options):
        self.stdout.write("Starting Kafka consumers...")
        payment_thread = Thread(target=listen_to_payment_topic)
        product_thread = Thread(target=listen_to_product_topic)
        
        payment_thread.start()
        product_thread.start()

        payment_thread.join()
        product_thread.join()
