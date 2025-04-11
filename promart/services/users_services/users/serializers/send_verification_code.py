from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import VerificationCode
from services.auth import create_verification_code

User = get_user_model()


class SendVerificationCodeSerializer(serializers.Serializer):
    """
    Serializer for sending a verification code to the provided email address.
    
    Validates the email and creates a verification code.
    """
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        """
        Validates the email address. 
        
        - If the email is already registered, raise a ValidationError.
        - If an existing verification code exists for the email, delete it.
        
        Args:
            value (str): The email address to be validated.

        Returns:
            str: The validated email address.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered. "
                "If you've forgotten your password, use the \"Reset Password\" section."
            )
        
        VerificationCode.objects.filter(email=value).delete()
        return value

    def create(self, validated_data: dict) -> dict:
        """
        Creates and sends a verification code to the given email address.
        
        Args:
            validated_data (dict): The validated data containing the email.

        Returns:
            dict: A dictionary containing the email and a success message.
        """
        email = validated_data["email"]
        create_verification_code(email)
        return {"email": email, "message": "Verification code sent."}