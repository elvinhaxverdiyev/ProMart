from django.db import models

class ProductCache(models.Model):
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ProductCache(product_id={self.product_id}, name={self.name}, price={self.price})"