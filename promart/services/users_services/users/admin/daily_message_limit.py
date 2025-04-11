from django.contrib import admin
from django.utils.timezone import localtime, timedelta 
from ..models import DailyMessageLimit


@admin.register(DailyMessageLimit)
class DailyMessageLimitAdmin(admin.ModelAdmin):
    """
    Admin interface for managing DailyMessageLimit model.
    Allows setting a daily message limit and reset times.
    """
    
    list_display = (
        "limit", 
        "get_expiration_time", 
        "get_reset_time"
    )
    list_editable = (
        "limit",
    ) 
    list_display_links = (
        "get_expiration_time", 
        "get_reset_time"
    )  
    readonly_fields = (
        "id",
    ) 
    fieldsets = (
        ("General Settings", {
            "fields": (
                "limit", 
                "expiration_time", 
                "reset_time"
            ),
            "description": "Set a daily message limit and reset time."
        }),
    )

    def get_expiration_time(self, obj: DailyMessageLimit) -> str:
        """
        Retrieves and formats the expiration time for the daily message limit.

        Args:
            obj (DailyMessageLimit): The model instance.

        Returns:
            str: Formatted expiration time as a string.
        """
        return self.format_duration(obj.expiration_time)
    get_expiration_time.short_description = "Code Expiration Date"

    def get_reset_time(self, obj: DailyMessageLimit) -> str:
        """
        Retrieves and formats the reset time for the daily message limit.

        Args:
            obj (DailyMessageLimit): The model instance.

        Returns:
            str: Formatted reset time as a string.
        """
        return self.format_duration(obj.reset_time)
    get_reset_time.short_description = "Limit Reset Period"

    def format_duration(self, duration: timedelta) -> str:
        """
        Converts a timedelta object into a human-readable string.

        Args:
            duration (timedelta): The duration to format.

        Returns:
            str: A human-readable string representing the duration.
        """
        total_seconds = int(duration.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = [
            f"{days} day" if days else "",
            f"{hours} hour" if hours else "",
            f"{minutes} minute" if minutes else "",
            f"{seconds} second" if seconds else ""
        ]
        return " ".join(filter(None, parts)) or "0 second"