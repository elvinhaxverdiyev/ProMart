from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    )
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default="buyer")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email