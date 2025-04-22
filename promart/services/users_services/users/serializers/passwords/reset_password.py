from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import VerificationCode

__all__ = [
    "ResetPasswordSerializer"
]

User = get_user_model()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for handling the password reset process.
    Validates the email, verification code, and new password.
    """
    email = serializers.EmailField()
    verification_code = serializers.CharField(
        min_length=6, 
        max_length=6
    )
    new_password = serializers.CharField(
        write_only=True
    )

    def validate(self, data: dict) -> dict:
        """
        Validate the provided data to ensure the verification code 
        is correct and not expired.
        
        Args:
            data (dict): The input data containing email, verification_code, 
            and new_password.
        
        Returns:
            dict: The validated data if everything is correct.
        
        Raises:
            serializers.ValidationError: If the verification code is 
            invalid or expired.
        """
        email = data["email"]
        verification_code = data["verification_code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User not found."}
            )

        try:
            record = VerificationCode.objects.get(
                email=email,
                verification_code=verification_code
            )
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError(
                {"verification_code": "Invalid or expired verification code."}
            )

        if record.is_verified or record.is_expired():
            raise serializers.ValidationError(
                {"verification_code": "Verification code is invalid or expired."}
            )

        return data

    def create(self, validated_data: dict) -> User:
        """
        Create a new password for the user after validation.
        
        Args:
            validated_data (dict): The validated data containing 
            email and new password.
        
        Returns:
            User: The updated user object with the new password set.
        """
        email = validated_data["email"]
        new_password = validated_data["new_password"]
        
        # We find the user by email
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Mark the verification code as used
        VerificationCode.objects.filter(
            email=email
        ).update(is_verified=True)

        return user