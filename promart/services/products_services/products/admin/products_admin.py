from django.contrib import admin
from ..models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "price", "stock", 
        "status", "is_active", "create_at", 
        "expire_at"
    )
    list_filter = ("status", "is_active", "category")
    search_fields = ("name", "description")
    filter_horizontal = ("category",)
    ordering = ("-create_at",)
    readonly_fields = ("create_at",)

    fieldsets = (
        (None, {
            "fields": (
                "user_id", "name", "description", "price", 
                "image", "category", "stock"
            )
        }),
        ("Status and Availability", {
            "fields": ("is_active", "status", "expire_at")
        }),
        ("Timestamps", {
            "fields": ("create_at",)
        }),
    )
