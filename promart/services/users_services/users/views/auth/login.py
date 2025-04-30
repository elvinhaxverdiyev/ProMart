import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.serializers import LoginSerializer
from users.kafka.producer import send_message
from utils.redis_client import redis_client
from django.contrib.auth import get_user_model

__all__ = ["LoginView"]

logger = logging.getLogger(__name__)
User = get_user_model()


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="Authenticate a user using email/username and password.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful. Returns user info or token.",
                examples={
                    "application/json": {
                        "refresh": "abc123refresh",
                        "access": "xyz456access",
                        "user": {
                            "id": 1,
                            "username": "johndoe",
                            "email": "john@example.com"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Login failed due to invalid credentials.",
                examples={
                    "application/json": {
                        "non_field_errors": ["Invalid email or password."]
                    }
                }
            ),
        },
        tags=["Users"]
    )
    def post(self, request) -> Response:
        logger.info("Login request received")
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Kafka
            try:
                send_message(user.id)
                logger.info(f"User data sent to Kafka: {user.email}")
            except Exception as e:
                logger.error(f"Kafka error during login: {e}")

            # Redis
            try:
                redis_client.hset(f"user:{user.id}", mapping={
                    "email": user.email,
                    "username": user.username,
                    "phone_number": user.phone_number or "",
                    "user_type": user.user_type or "",
                    "profile_picture": user.profile_picture.url if user.profile_picture else ""
                })
                logger.info(f"User data cached in Redis: user:{user.id}")
            except Exception as e:
                logger.error(f"Redis error during login: {e}")

            return Response({
                "refresh": serializer.validated_data["refresh"],
                "access": serializer.validated_data["access"],
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }, status=status.HTTP_200_OK)

        logger.warning("Login failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
