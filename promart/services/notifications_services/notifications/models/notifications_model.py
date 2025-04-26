from django.db import models

# Create your models here.

class Notifications(models.Model):
    user = models.IntegerField()
    telegram = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username