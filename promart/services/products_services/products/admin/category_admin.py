from django.utils.html import format_html
from django.contrib import admin
from ..models import Category
from django.db.models import QuerySet
from typing import Any


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Category model.

    This class provides custom functionality for displaying categories, 
    filtering, searching, and actions such as activating and deactivating categories.
    """
    
    list_display = (
        "get_subcategory",  
        "get_super_category_name", 
        "order",
        "is_active",
        "icon_preview",
    )
    list_filter = (
        "is_active",
        "super_category"
    )
    search_fields = (
        "name",
    )
    ordering = (
        "super_category",
        "order"
    )
    actions = [
        "activate_categories", 
        "deactivate_categories"
    ]

    def get_subcategory(self, obj: Category) -> str:
        """
        Returns the name of the subcategory if it has a super category, 
        otherwise returns "-".
        """
        return obj.name if obj.super_category else "-"
    get_subcategory.short_description = "Subcategory"
    
    def get_super_category_name(self, obj: Category) -> str:
        """
        Returns the name of the super category if it exists, otherwise 
        returns the category"s own name.
        """
        return obj.super_category.name if obj.super_category else obj.name
    get_super_category_name.short_description = "Super Category"

    def icon_preview(self, obj: Category) -> str:
        """
        Shows a preview of the category"s icon in the admin panel. If no icon 
        is set, returns "No Image".
        """
        if obj.icon:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 10px;" />', 
                obj.icon.url
            )
        return "No Image"
    icon_preview.short_description = "Icon Preview"  

    def activate_categories(self, request: Any, queryset: QuerySet) -> None:
        """
        Activates the selected categories.
        """
        queryset.update(is_active=True)
    activate_categories.short_description = "Activate selected categories"

    def deactivate_categories(self, request: Any, queryset: QuerySet) -> None:
        """
        Deactivates the selected categories.
        """
        queryset.update(is_active=False)
    deactivate_categories.short_description = "Deactivate selected categories"

    def get_order_display(self, obj: Category) -> str:
        """
        Returns the order of the category if assigned, otherwise returns "Not assigned".
        """
        return obj.order if obj.order is not None else "Not assigned"
    get_order_display.short_description = "Order"

    def save_model(self, request: Any, obj: Category, form: Any, change: bool) -> None:
        """
        Ensures that the order is assigned before saving. If it"s not set, gets 
        the next order.
        """
        if obj.order is None:
            obj.order = obj.get_next_order() 
        super().save_model(request, obj, form, change)

    class SubCategoryInline(admin.TabularInline):
        """
        Inline representation for subcategories in the admin panel.
        """
        model = Category
        fk_name = "super_category"
        extra = 1
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    inlines = [SubCategoryInline]