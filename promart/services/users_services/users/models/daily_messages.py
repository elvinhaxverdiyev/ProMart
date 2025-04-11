from django.db import models
from django.utils.timezone import now
from users.models.daily_message_limit import DailyMessageLimit  


class DailyMessage(models.Model):
    """
    A model to represent the daily messages sent to users, 
    enforcing limits and expiration times.
    
    Attributes:
        email (str): The email address to which the message is sent.
        message_sent_at (datetime): The timestamp of when the message was sent.
    """

    email = models.EmailField()
    message_sent_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [models.Index(fields=["email"])]

    def __str__(self) -> str:
        """
        Returns a string representation of the message sent to the given email.
        
        Returns:
            str: The message sent information, including email and timestamp.
        """
        return f"Message sent to {self.email} at {self.message_sent_at}"

    @staticmethod
    def format_remaining_time(seconds: int) -> str:
        """
        Formats the remaining time into hours, minutes, and seconds.
        
        Args:
            seconds (int): The time in seconds to be formatted.
        
        Returns:
            str: The formatted time in "hh:mm:ss" format.
        """
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}:{minutes}:{seconds}"

    @classmethod
    def get_limit_info(cls) -> DailyMessageLimit:
        """
        Retrieves the daily message limit settings.
        
        Returns:
            DailyMessageLimit: The daily message limit settings.
        """
        limit_obj, _ = DailyMessageLimit.objects.get_or_create(id=1)
        return limit_obj

    @classmethod
    def clear_old_messages(cls, email: str, reset_time: int) -> None:
        """
        Deletes old messages if the reset time has passed.
        
        Args:
            email (str): The email of the user whose messages need to be cleared.
            reset_time (int): The duration after which old messages should be deleted.
        """
        first_message = cls.objects.filter(
            email=email).order_by("message_sent_at").first()

        if first_message and (now() - first_message.message_sent_at >= reset_time):
            cls.objects.filter(email=email).delete()

    @classmethod
    def check_daily_limit(cls, email: str, limit: int, reset_time: int) -> str | None:
        """
        Checks if the user has reached the daily message limit.
        
        Args:
            email (str): The email of the user.
            limit (int): The daily message limit.
            reset_time (int): The duration after which the limit resets.
        
        Returns:
            str | None: A message indicating the limit reached or None if within the limit.
        """
        today_messages_count = cls.objects.filter(
            email=email, message_sent_at__date=now().date()
        ).count()

        if today_messages_count >= limit:
            first_message_today = cls.objects.filter(
                email=email, 
                message_sent_at__date=now().date()
            ).order_by("message_sent_at").first()

            if first_message_today:
                remaining_time = (first_message_today.message_sent_at + reset_time) - now()
                seconds_remaining = max(int(remaining_time.total_seconds()), 0)
                return (
                    "You have reached your daily message limit. "
                    f"Please try again in {cls.format_remaining_time(seconds_remaining)} minutes."
                )

            return "You have reached your daily verification code limit, please try again later."

        return None

    @classmethod
    def check_expiration_time(cls, last_message: "DailyMessage", expiration_time: int) -> str | None:
        """
        Checks if the last message was sent within the expiration time.
        
        Args:
            last_message (DailyMessage): The last message sent to the user.
            expiration_time (int): The expiration time in seconds.
        
        Returns:
            str | None: A message indicating the remaining time to wait, or None if within expiration time.
        """
        if last_message:
            time_diff = now() - last_message.message_sent_at
            
            if time_diff < expiration_time:
                seconds_remaining = (expiration_time - time_diff).seconds
                return f"Please, try again in {cls.format_remaining_time(seconds_remaining)} seconds."

        return None

    @classmethod
    def send_message(cls, email: str) -> str:
        """
        Handles message sending logic while enforcing daily limits.
        
        Args:
            email (str): The email of the user to whom the message is sent.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        limit_obj = cls.get_limit_info()
        reset_time = limit_obj.reset_time

        cls.clear_old_messages(email, reset_time)

        limit_message = cls.check_daily_limit(
            email, 
            limit_obj.limit, 
            reset_time
        )
        if limit_message:
            return limit_message

        last_message = cls.objects.filter(
            email=email).order_by("-message_sent_at").first()

        expiration_message = cls.check_expiration_time(
            last_message, 
            limit_obj.expiration_time
        )

        if expiration_message:
            return expiration_message

        cls.objects.create(email=email)
        return "Message sent successfully!"