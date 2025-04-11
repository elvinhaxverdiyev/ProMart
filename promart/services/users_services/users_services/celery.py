from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users_services.settings")

app = Celery("users_services")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    CELERY_POOL="solo",
)

app.autodiscover_tasks()








