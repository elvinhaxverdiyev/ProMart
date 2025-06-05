from django.db import models


class PaymentRequest(models.Model):
    cart_id = models.IntegerField()
    user_id = models.CharField(max_length=100)
    product_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    action = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.cart_id} - User {self.user_id}"
