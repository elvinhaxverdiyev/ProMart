import logging
from django.utils.timezone import now
from typing import Dict, Any

from users.models.daily_message_limit import DailyMessageLimit
from users.models.daily_messages import DailyMessage
from users.models import VerificationCode

from utils.verification_code import generate_verification_code
from users.tasks import send_verification_email

__all__ = ["reset_password_send_code"]

logger = logging.getLogger(__name__)

def reset_password_send_code(email: str) -> Dict[str, Any]:
    """
    Sends a verification code to the given email for password reset.
    
    Args:
        email (str): The email address to which the verification code should be sent.
    
    Returns:
        dict: A dictionary containing the email and a message indicating the status.
    """
    logger.info(f"Starting password reset process for email: {email}")
    
    # Get daily message limit
    limit_obj = DailyMessage.get_limit_info()
    reset_time = limit_obj.reset_time

    # Daily limit check
    limit_message = DailyMessage.check_daily_limit(
        email, 
        limit_obj.limit, 
        reset_time
    )

    if limit_message:
        logger.warning(f"Daily limit reached for email: {email}")
        return {"email": email, "message": limit_message}

    verification_code = generate_verification_code()
    logger.debug(
        f"Generated verification code: {verification_code} for email: {email}"
    )
    
    VerificationCode.objects.create(
        email=email, 
        verification_code=verification_code
    )
    logger.info(
        f"Verification code for {email} has been saved to the database."
    )
    
    send_verification_email.delay(email)
    logger.info(f"Verification email sent to {email}.")

    # Add the new message to the database
    DailyMessage.objects.create(email=email)
    
    return {"email": email, "message": "Verification code sent."}