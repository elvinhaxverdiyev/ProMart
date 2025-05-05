from django.urls import path
from orders.views import *

urlpatterns = [
    # Cart endpoints
    path(
        "orders/cart/", 
        ToggleCartView.as_view(), 
        name="cart-toggle"
    ),
]