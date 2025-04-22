import os
import django
import json
import logging
from kafka import KafkaConsumer
from django.conf import settings
from users.models import CustomUser

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users_services.settings")
django.setup()

# Configure logging
logger = logging.getLogger(__name__)

"""
Kafka Consumer Script for User Updates

This script listens to a Kafka topic for user data updates. When a message is received,
it tries to find the corresponding user in the database and update their fields based on the message content.
"""

# Create Kafka consumer
consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='user-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

logging.info("Kafka consumer started. Waiting for messages...")

# Start consuming messages from the Kafka topic
for message in consumer:
    data = message.value
    logging.info(f"Received message: {data}")

    user_id = data.get("user_id")
    if not user_id:
        logging.warning("Missing 'user_id' in the message. Skipping update.")
        continue

    try:
        user = CustomUser.objects.get(id=user_id)
        logging.info(f"User found (ID: {user_id}). Proceeding with update...")

        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.user_type = data.get("user_type", user.user_type)
        user.save()

        logging.info(f"User (ID: {user_id}) updated successfully.")
    except CustomUser.DoesNotExist:
        logging.warning(f"User not found (ID: {user_id}). Cannot perform update.")
    except Exception as e:
        logging.error(f"Unexpected error while updating user (ID: {user_id}): {e}")
