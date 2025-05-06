from django.urls import path
from payments.views.start_payment import PaymentSuccessView, PaymentCancelView


urlpatterns = [
    # Payment endpoints
    path(
        "orders/payment/success", 
        PaymentSuccessView.as_view(), 
        name="payment_success"
    ),
    path(
        "orders/payment/cancel", 
        PaymentCancelView.as_view(), 
        name="payment_cancel"
    )
    
]