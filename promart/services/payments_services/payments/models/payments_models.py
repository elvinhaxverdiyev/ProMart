from django.db import models


class Payment(models.Model):
    STATUS = (
        ("pending", "Pending"),         
        ("paid", "Paid"),       
        ("failed", "Failed")    
    )
    
    order_id = models.UUIDField()
    user_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)