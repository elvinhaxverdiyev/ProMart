from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.http import HttpRequest

from ..forms import CustomUserCreationForm, CustomUserChangeForm
from ..models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for managing the CustomUser model in the Django admin panel.
    """

    model = CustomUser
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "profile_picture_preview",
    ]
    list_filter = [
        "is_active", 
        "is_staff"
    ]
    search_fields = [
        "email", 
        "first_name", 
        "last_name"
    ]
    ordering = [
        "email"
    ]

    fieldsets = (
        (None, {"fields": (
            "email", 
            "password"
        )}),
        ("Personal info", {"fields": (
            "first_name", 
            "last_name", 
            "bio", 
            "profile_picture", 
        )}),
        ("Permissions", {"fields": (
            "is_active", 
            "is_staff", 
            "is_superuser", 
            "groups", 
            "user_permissions"
        )}),
        ("Important dates", {"fields": (
            "last_login", 
            "date_joined"
        )}),
    )

    add_fieldsets = (
        (None, {"fields": (
            "email", 
            "password1", 
            "password2"
        )}),
        ("Personal info", {"fields": (
            "first_name", 
            "last_name", 
            "bio", 
            "profile_picture", 
        )}),
        ("Permissions", {"fields": (
            "is_active", 
            "is_staff", 
            "is_superuser"
        )}),
    )

    filter_horizontal = ("groups", "user_permissions")

    def profile_picture_preview(self, obj: CustomUser) -> str:
        """
        Displays a small preview of the profile picture in the admin panel.

        Args:
            obj (CustomUser): The CustomUser instance.

        Returns:
            str: HTML string for displaying the profile picture or "No Image" 
            if not available.
        """
        if obj.profile_picture:
            try:
                return mark_safe(
                    f'<img src="{obj.profile_picture.url}" width="50" height="50" />'
                )
            except Exception as e:
                return "No Image"
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture"