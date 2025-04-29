from django.urls import path
from orders.views import *

urlpatterns = [
    path("orders/cart/", ToggleCartView.as_view(), name="cart-toggle"),
]