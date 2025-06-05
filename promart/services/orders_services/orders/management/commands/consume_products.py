import json
import logging
from kafka import KafkaConsumer
from django.core.management.base import BaseCommand
from orders.models import ProductReplica
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Consume product data from Kafka and save to ProductReplica model"

    def handle(self, *args, **options):
        kafka_topic = os.getenv("KAFKA_PRODUCT_TOPIC", "products_topic")
        kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

        consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="order-service-group"
        )

        self.stdout.write(self.style.SUCCESS("Kafka consumer started..."))

        for message in consumer:
            product_data = message.value
            product_id = product_data.get("id")

            # DB-yə yaz
            ProductReplica.objects.update_or_create(
                product_id=product_id,
                defaults={
                    "name": product_data.get("name"),
                    "description": product_data.get("description"),
                    "price": product_data.get("price"),
                    "stock": product_data.get("stock"),
                    "status": product_data.get("status"),
                    "user_id": product_data.get("user_id"),
                    "image": product_data.get("image"),
                }
            )

            logger.info("Product saved: %s", product_id)
