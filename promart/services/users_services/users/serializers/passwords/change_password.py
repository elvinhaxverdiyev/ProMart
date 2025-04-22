from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

__all__ = [
    "ChangePasswordSerializer"
]

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to handle the password change process, including validating
    the old password, ensuring the new password matches the confirmation, 
    and updating the user's password.
    """
    old_password = serializers.CharField(
        write_only=True
    )
    new_password = serializers.CharField(
        write_only=True
    )
    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, data: dict) -> dict:
        """
        Validates the password change request, checking if the old password
        is correct and if the new password matches the confirmation password.

        Args:
            data (dict): Dictionary containing old_password, new_password, 
                         and confirm_password.

        Raises:
            ValidationError: If the old password is incorrect or the new 
                             password doesn’t match the confirmation.

        Returns:
            dict: Validated data for password change.
        """
        user = self.context["request"].user 
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # Check if old password is correct
        if not user.check_password(old_password):
            raise ValidationError(
                {"old_password": "The old password is incorrect."}
            )

        # Check if new password matches confirm password
        if new_password != confirm_password:
            raise ValidationError(
                {"new_password": "The new password and confirm password do not match."}
            )

        return data

    def create(self, validated_data: dict) -> User:
        """
        Creates and saves the new password for the user.

        Args:
            validated_data (dict): Dictionary containing the new password.

        Returns:
            User: The updated user instance after changing the password.
        """
        user = self.context["request"].user
        user.set_password(validated_data["new_password"])
        user.save()
        return user