from django.db import models
from .products_models import Product
from django.conf import settings
from typing import List


class Comment(models.Model):
    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.CASCADE, 
        related_name="comments"
    ) 
    user = models.IntegerField()
    
    text = models.TextField()
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]  
    
    def __str__(self) -> str:
        return f"User {self.user} - {self.text[:30]}"

    