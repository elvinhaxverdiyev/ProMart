from django.urls import path

from products.views import *

urlpatterns = [
    path(
        "products",
        ProductsListAPIView.as_view(),
        name="products-list"
    ),
    path(
        "products/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail"
    ),
]

