from django.db import models
from django.utils.timezone import now


class VerificationCode(models.Model):
    """
    Model for storing email verification codes.

    This model stores the email, the verification code, its verification status, 
    and the timestamp when it was created. It also includes methods to check 
    if the code has expired.
    """
    email = models.EmailField()
    verification_code = models.CharField(
        max_length=6
    )
    is_verified = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["verification_code"]),
        ]

    def __str__(self) -> str:
        """
        Returns a string representation of the VerificationCode instance.
        
        Returns:
            str: A message containing the email associated with the verification code.
        """
        return f"Verification code for {self.email}"
    
    def is_expired(self) -> bool:
        """
        Checks if the verification code has expired (3 minutes).

        Returns:
            bool: True if the verification code is expired, otherwise False.
        """
        return (now() - self.created_at).total_seconds() > 180