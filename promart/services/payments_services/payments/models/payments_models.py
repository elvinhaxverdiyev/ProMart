from django.db import models


class Payment(models.Model):
    order_id = models.IntegerField()  
    user_id = models.IntegerField()
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    status = models.CharField(
        max_length=20, 
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled")
        ], 
        default="pending"
    )
    payment_method = models.CharField(
        max_length=50, 
        default="paypal"
    )
    paypal_payment_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Pay(order_id={self.order_id}, user_id={self.user_id}, status={self.status})"