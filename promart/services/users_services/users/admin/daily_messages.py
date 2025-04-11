from django.contrib import admin
from django.utils.timezone import localtime, timedelta 
from ..models import DailyMessage


@admin.register(DailyMessage)
class DailyMessageAdmin(admin.ModelAdmin):
    """
    Admin class for DailyMessage model to manage the display and behavior in Django admin.
    """
    
    list_display = (
        "email", 
        "local_message_sent_at"
    )
    list_filter = (
        "message_sent_at",
    )
    search_fields = (
        "email",
    )
    readonly_fields = (
        "message_sent_at",
    )

    def local_message_sent_at(self, obj: DailyMessage) -> str:
        """
        Converts the message_sent_at field to the local time zone and formats it as a string.
        
        Args:
            obj (DailyMessage): The instance of the DailyMessage model.
        
        Returns:
            str: The formatted local time for message_sent_at.
        """
        return localtime(obj.message_sent_at).strftime("%Y-%m-%d %H:%M:%S")

    local_message_sent_at.admin_order_field = "message_sent_at"
    local_message_sent_at.short_description = "Local Time"