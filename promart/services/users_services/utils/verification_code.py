import random
import logging

__all__ = ["generate_verification_code"]

logger = logging.getLogger(__name__)


def generate_verification_code() -> str:
    """
    Generate a 6-digit random verification code.
    
    Returns:
        str: A randomly generated 6-digit verification code as a string.
    """
    code: str = str(random.randint(100000, 999999))
    logger.info(f"Generated verification code: {code}")
    return code