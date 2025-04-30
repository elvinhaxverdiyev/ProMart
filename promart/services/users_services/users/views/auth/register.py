import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import RegisterSerializer
from users.kafka.producer import send_message
from utils.redis_client import redis_client

__all__ = ["RegisterView"]

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(APIView):
    """
    API view for registering a new user.

    This endpoint allows new users to register by submitting their information
    via a multipart/form-data request. Upon successful registration, user data
    is sent to Kafka and also saved to Redis for quick access.
    """

    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="User registration endpoint",
        operation_summary="Register a new user",
        consumes=["multipart/form-data"],
        tags=["Users"]
    )
    def post(self, request):
        logger.info("Registration request received with data: %s", request.data)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info("User created with ID: %s", user.id)

            # Kafka
            try:
                send_message(user.id)
                logger.info("Sent user data to Kafka for user: %s", user.email)
            except Exception as e:
                logger.error("Failed to send Kafka message: %s", str(e))

            # Redis
            try:
                redis_key = f"user:{user.id}"
                redis_client.hset(redis_key, mapping={
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username or "",
                    "phone_number": user.phone_number or "",
                    "user_type": user.user_type or "",
                    "profile_picture": user.profile_picture.url if user.profile_picture else ""
                })
                logger.info("Saved user data to Redis: %s", redis_key)
            except Exception as e:
                logger.error("Failed to save user data to Redis: %s", str(e))

            logger.info("Registration successful for user: %s", user.email)
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)

        logger.warning("Registration failed with errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
