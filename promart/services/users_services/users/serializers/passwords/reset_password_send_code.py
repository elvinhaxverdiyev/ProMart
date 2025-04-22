from django.contrib.auth import get_user_model
from rest_framework import serializers

from services.auth import reset_password_send_code

__all__ = [
    "ResetPasswordSendCodeSerializer"
]

User = get_user_model()


class ResetPasswordSendCodeSerializer(serializers.Serializer):
    """
    Serializer for sending a password reset code to the user's email.
    Takes the email and validates if the user exists. If valid, sends the reset code.
    """
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        """
        Validates the provided email. Checks if the user exists in the system.

        Args:
            value (str): The email to validate.

        Returns:
            str: The validated email if the user exists.

        Raises:
            serializers.ValidationError: If the user does not exist.
        """
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist."
            )

        self.user = user
        return value

    def create(self, validated_data: dict) -> None:
        """
        Creates a password reset request by sending a reset code to the user's email.

        Args:
            validated_data (dict): The validated data, which includes the user information.

        Returns:
            None: This method triggers the external function to send the reset code.
        """
        return reset_password_send_code(self.user.email)