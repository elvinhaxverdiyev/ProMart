from django.db import models
from django.utils.timezone import timedelta
from typing import Optional


class DailyMessageLimit(models.Model):
    """
    A model that defines a daily message limit configuration,
    including the maximum number of messages, expiration time 
    for each message, and the reset time for the daily limit.
    """
    limit = models.PositiveIntegerField(
        default=3
    )  
    expiration_time = models.DurationField(
        default=timedelta(minutes=3)
    )  
    reset_time = models.DurationField(
        default=timedelta(hours=24)
    )  

    def __str__(self) -> str:
        """
        Returns a string representation of the daily message limit configuration.
        """
        return (
            f"Daily Limit: {self.limit} "
            f"Expiration Time: {self.expiration_time} "
            f"Reset Time: {self.reset_time}"
        )