from django.urls import path
from payments.views.start_payment import CreatePayPalPaymentView

urlpatterns = [
    path("api/paypal/create/", CreatePayPalPaymentView.as_view(), name="paypal-create"),
]
