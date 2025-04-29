from celery import shared_task
from django.utils import timezone
from .models import Product

@shared_task
def remove_expired_products():
    now = timezone.now()
    expired_products = Product.objects.filter(expire_at__lt=now)
    count = expired_products.count()
    expired_products.delete()
    return f"{count} expired products deleted."
