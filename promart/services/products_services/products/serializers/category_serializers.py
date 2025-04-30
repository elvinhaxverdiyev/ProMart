from rest_framework import serializers
from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer includes a computed field `super_category_name`, which retrieves
    the name of the related super category using the `get_super_category_name` method.
    """
    super_category_name = serializers.CharField(
        source="get_super_category_name", 
        read_only=True
    )
    
    class Meta:
        model = Category
        fields = (
            "id", 
            "name", 
            "icon", 
            "order", 
            "is_active", 
            "super_category", 
            "super_category_name"
        )


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the SubCategory model.

    This serializer ensures that the `super_category` field is required,
    enforcing that every subcategory is linked to a parent category.
    """

    class Meta:
        model = Category
        fields = (
            "id", 
            "name", 
            "icon", 
            "order", 
            "is_active", 
            "super_category"
        )
       