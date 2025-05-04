from rest_framework import serializers
from orders.models.cart_model import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id", 
            "user_id", 
            "product_id", 
            "quantity", 
            "added_at"
        ]
        read_only_fields = [
            "id", 
            "added_at"
        ]
