from kafka import KafkaConsumer
import json
from django.conf import settings
from users.models import CustomUser #burda nie custom user import elemisik

# Create a Kafka consumer
consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,  # Kafka topic name
    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],  # Kafka server connections
    auto_offset_reset='earliest',  # Messages are read from the beginning
    enable_auto_commit=True,  # Kafka automatically commits messages
    group_id='product-group',  # Kafka consumer group name
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize incoming messages from JSON format
)

print("Kafka consumer started. Waiting for messages...")

# Read messages from the Kafka topic
for message in consumer:
    data = message.value  # Get the data from the Kafka message
    print("Received message:", data)

    user_id = data.get("user_id")  # Extract user ID from the message
    try:
        # Find the user by ID
        user = CustomUser.objects.get(id=user_id)  
        print(f"User found: {user_id}")

        # Update user details based on the incoming Kafka message
        user.email = data.get("email", user.email)  # Update email if provided
        user.phone_number = data.get("phone_number", user.phone_number)  # Update phone number if provided
        user.user_type = data.get("user_type", user.user_type)  # Update user type if provided
        user.save()  # Save the changes to the user object
        print(f"User updated: {user_id}")
    except CustomUser.DoesNotExist:
        # If user is not found, print a message
        print(f"User not found: {user_id}")
