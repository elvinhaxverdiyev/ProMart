from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import VerificationCode
from services.auth import validate_verification_code

User = get_user_model()

__all__ = [
    "RegisterSerializer"
]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    
    This serializer validates and processes user registration data,
    including email verification.
    """
    email = serializers.EmailField()
    verification_code = serializers.CharField(
        min_length=6, 
        max_length=6
    )
    first_name = serializers.CharField(
        max_length=30
    )
    last_name = serializers.CharField(
        max_length=30
    )
    password = serializers.CharField(
        write_only=True
    )   
    profile_picture = serializers.ImageField(
        required=False
    )
    user_type = serializers.CharField(
        
    )
        
    class Meta:
        model = User
        fields = [
            "email", 
            "verification_code", 
            "first_name", 
            "last_name", 
            "password", 
            "profile_picture",
            "user_type"
        ]
    
    def validate_email(self, value):
        """
        Check if the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value

    def validate(self, data: dict) -> dict:
        """
        Validates the registration data by checking the verification code.
        """
        try:
            validate_verification_code(
                data["email"], 
                data["verification_code"]
            )
        except ValueError as e:
            raise serializers.ValidationError(
                {"verification_code": str(e)}
            )

        return data

    def create(self, validated_data: dict) -> User:
        """
        Creates a new user instance with the validated data.
        """
        email = validated_data["email"]
        validated_data.pop("verification_code")

        # Check if email is already registered before creating a new user
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "This email is already registered."}
            )

        # Create a new user
        user = User.objects.create_user(**validated_data)
        
        # Mark the verification code as verified
        VerificationCode.objects.filter(
            email=email).update(is_verified=True)

        return user
    