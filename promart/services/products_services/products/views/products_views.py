import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from products.models import Product
from products.serializers import ProductSerializer
from utils.permissions import is_seller

logger = logging.getLogger(__name__)

__all__ = ["ProductsListAPIView",
           "ProductDetailAPIView"
        ]

class ProductsListAPIView(APIView):
    """
    API endpoint for listing all products and creating a new product.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Returns a list of all available products.",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=ProductSerializer(many=True)
            )
        }
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Allows sellers to create new products. Only users with 'seller' user_type can perform this action.",
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Product successfully created",
                schema=ProductSerializer()
            ),
            400: "Bad request",
            403: "Forbidden - Only sellers can create products",
        }
    )
    def post(self, request):
        user_id = request.user.id

        # if not is_seller(user_id):
        #     logger.warning(f"User {user_id} ya Redis-də tapılmadı, ya da 'seller' deyil.")
        #     return Response({"detail": "Only sellers can create products."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(user_id=user_id)
            logger.info(f"Yeni məhsul yaradıldı: {product.name} (user_id={user_id})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning("Məhsul yaratmaq uğursuz oldu: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, product_id):
        
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)