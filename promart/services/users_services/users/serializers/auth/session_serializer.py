from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from services.auth.tokens import get_tokens_for_user

__all__ = [
    "LoginSerializer",
    "LogoutSerializer"
]


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login to authenticate and generate JWT tokens.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict) -> dict:
        """
        Validates the provided email and password and generates JWT tokens.
        """
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email, 
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")


        tokens = get_tokens_for_user(user)

        return {
            "user": user,
            "refresh": tokens["refresh"],
            "access": tokens["access"]
        }


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout to handle the refresh token.
    """
    refresh = serializers.CharField()