from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils.paypal import create_paypal_order

class CreatePayPalPaymentView(APIView):
    def post(self, request):
        # Məsələn, request.body-də cart_id olur
        cart_id = request.data.get("cart_id")

        # Əvəzində burda sebetdən məhsulları çıxarırsan:
        # Burda nümunə üçün hardcoded
        cart_items = [
            {
                "product_name": "Example Product 1",
                "quantity": 2,
                "price": "149.99"
            },
            {
                "product_name": "Example Product 2",
                "quantity": 1,
                "price": "89.50"
            }
        ]

        # Total hesablayırıq
        total = sum(float(item["price"]) * item["quantity"] for item in cart_items)

        try:
            order_response = create_paypal_order(cart_items, total)

            # approval URL-i çıxarırıq
            approval_url = next(
                (link["href"] for link in order_response["links"] if link["rel"] == "approve"),
                None
            )

            if not approval_url:
                return Response({"error": "Approval URL not found"}, status=500)

            return Response({"approval_url": approval_url})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
