import os
from celery import shared_task
from django.core.mail import send_mail

from users.models import VerificationCode
from services.auth.email_services import create_verification_code


@shared_task
def send_verification_email(email: str) -> str:
    """
    Sends a verification email with a generated verification code to the given email address.

    Args:
        email (str): The email address to which the verification code will be sent.

    Returns:
        str: A success message indicating that the email has been sent.
    """
    verification_code = create_verification_code(email)
    sender_email = os.getenv("EMAIL_HOST_USER")

    send_mail(
        "Email Verification",
        f"Your verification code is: {verification_code}",
        sender_email,
        [email],
        fail_silently=False,
    )

    return f"Verification email sent successfully to {email}"