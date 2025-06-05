from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    user_id = models.IntegerField()
    order_id = models.IntegerField()
    paypal_order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} | Order: {self.order_id} | Status: {self.status}"
