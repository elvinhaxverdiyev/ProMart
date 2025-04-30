from rest_framework import serializers
from products.models import Product
# from utils.ai_helper import generate_product_description  


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Product model.
    
    This serializer is used for creating, updating, and retrieving product instances.
    It also automatically generates a product description if none is provided.
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["user_id", "expire_at"]

    # def create(self, validated_data):
    #     """
    #     Creates a new product instance.

    #     If the product does not have a description, it will automatically generate one
    #     using the product's name through the AI-based `generate_product_description` function.

    #     Args:
    #         validated_data (dict): Data validated by the serializer.

    #     Returns:
    #         Product: The newly created product instance.
    #     """
    #     product = super().create(validated_data)
        
    #     # If no description is provided, generate one using AI
    #     if not product.description:
    #         product.description = generate_product_description(product.name)
    #         product.save()
        
    #     return product

    # def update(self, instance, validated_data):
    #     """
    #     Updates an existing product instance.

    #     If the product does not have a description, it will automatically generate one
    #     using the product's name through the AI-based `generate_product_description` function.

    #     Args:
    #         instance (Product): The product instance to be updated.
    #         validated_data (dict): Data validated by the serializer.

    #     Returns:
    #         Product: The updated product instance.
    #     """
    #     product = super().update(instance, validated_data)
        
    #     # If no description is provided, generate one using AI
    #     if not product.description:
    #         product.description = generate_product_description(product.name)
    #         product.save()
        
    #     return product
