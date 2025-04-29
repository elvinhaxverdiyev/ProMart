from django.db import models
from datetime import timedelta
from django.utils import timezone

from .category_models import Category


class Product(models.Model):
    STATUS = (
        ("active", "Active"),         
        ("pending", "Pending"),       
        ("sold_out", "Sold Out"),     
        ("inactive", "Inactive"),    
    )

    user_id = models.IntegerField()
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True
    )
    category = models.ManyToManyField(
        Category
    )
    stock = models.PositiveIntegerField(
        default=0
    )
    is_active = models.BooleanField(
        default=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="inactive"
    )
    create_at = models.DateTimeField(
        auto_now=True
    )
    expire_at = models.DateTimeField()

    def __str__(self):
        return self.name or f"Product #{self.id}"

    def save(self, *args, **kwargs):
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)