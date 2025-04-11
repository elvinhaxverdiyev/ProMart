import random
import logging
from django.contrib.auth import get_user_model
from users.models import VerificationCode

__all__ = [
    "validate_verification_code"
]

logger = logging.getLogger(__name__)

User = get_user_model() 


def validate_verification_code(email: str, verification_code: str) -> VerificationCode:
    """
    Checks whether the provided email address and stored code are correct and valid.

    :param email: The user's email address.
    :param verification_code: The sent deletion code.
    :return: Returns a VerificationCode object if the code is valid.
    :raises ValueError: If the code is invalid or has already been used.
    """
    logger.info(f"Validating verification code for email: {email}")
    try:
        record = VerificationCode.objects.get(
            email=email, 
            verification_code=verification_code
        )
    except VerificationCode.DoesNotExist:
        logger.warning(f"Invalid or expired verification code for email: {email}")
        raise ValueError("Invalid or expired verification code.")
    
    if record.is_verified or record.is_expired():
        logger.warning(
            f"Verification code for email: {email} is either already verified or expired."
        )
        raise ValueError("Verification code is invalid or expired.")
    
    logger.info(f"Verification code for email: {email} is valid.")
    return record