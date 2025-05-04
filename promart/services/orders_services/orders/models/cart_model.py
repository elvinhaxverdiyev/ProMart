from django.conf import settings
from django.db import models


class Cart(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CartItem(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})"

    @classmethod
    def toggle_cart(cls, user: settings.AUTH_USER_MODEL, product_id: int) -> bool:
        """
        Toggles the cart status for a product.

        If the product is not in the user's cart, it adds it.
        If the product is already in the user's cart, it removes it.

        Returns:
            bool: True if added, False if removed.
        """
        cart_item, created = cls.objects.get_or_create(user_id=user.id, product_id=product_id)
        if created:
            return True, cart_item
        
        cart_item.delete()
        return False, None


