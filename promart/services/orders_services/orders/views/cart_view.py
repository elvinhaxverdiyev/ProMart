from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from orders.models.cart_model import Cart
from orders.serializers.cart_serializers import CartSerializer
from orders.kafka.producer import send_order_to_payment_topic
from orders.models.product_replica import ProductReplica

__all__ = [
    "ToggleCartView",
]


class ToggleCartView(APIView):

    permission_classes = [IsAuthenticated]  

    @swagger_auto_schema(
        operation_summary="List cart items",
        operation_description="""        
        Returns a list of products in the user's cart.
        """,
        tags=["Cart"],
        responses={
            200: openapi.Response(
                description="Cart items retrieved successfully.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "user": 5,
                            "product": 12,
                            "quantity": 1,
                            "added_at": "2025-04-29T10:00:00Z"
                        }
                    ]
                }
            ),
            401: openapi.Response("Unauthorized: User not authenticated.", examples={"application/json": {"error": "Unauthorized: User not authenticated."}}),
        }
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized: User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        cart_items = Cart.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Toggle product in cart",
        operation_description="""        
        - Adds the product if it is not already in the cart.
        - Removes the product if it is already in the cart.
        """,
        tags=["Cart"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["product_id"],
            properties={
                "product_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product"),
            },
        ),
        responses={
            201: openapi.Response(
                "Product added to cart.", 
                examples={"application/json": {"message": "Product added to cart."}}
            ),
            200: openapi.Response(
                "Product removed from cart.", 
                examples={"application/json": {"message": "Product removed from cart."}}
            ),
            400: openapi.Response(
                "Bad Request: Product ID is required.", 
                examples={"application/json": {"error": "Product ID is required."}}
            ),
            401: openapi.Response(
                "Unauthorized: User not authenticated.", 
                examples={"application/json": {"error": "Unauthorized: User not authenticated."}}
            ),
        }
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized: User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get("product_id")
        
        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        success, cart_item = Cart.toggle_cart(user=request.user, product_id=product_id)

        product = ProductReplica.objects.filter(product_id=product_id).first()

        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        send_order_to_payment_topic({
            "user_id": str(request.user.id),
            "product_id": product_id,
            "cart_id": cart_item.id if cart_item else None,
            "price": str(product.price),
            "quantity": cart_item.quantity if cart_item else None,
            "action": "added" if success else "removed"
        })

        if success:
            return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
