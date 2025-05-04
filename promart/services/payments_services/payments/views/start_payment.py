import paypalrestsdk
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models.payments_models import Payment
import logging

logger = logging.getLogger(__name__)

# Configure PayPal SDK with client ID and secret from settings
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


class PaymentSuccessView(APIView):
    """
    View to handle successful PayPal payments.
    It retrieves payment details and updates the payment status in the database.
    """
    def get(self, request):
        """
        Handles the GET request for successful payments.

        Parameters:
        - paymentId: PayPal payment ID
        - PayerID: PayPal payer ID
        - cart_id: The cart or order ID related to the payment
        
        Returns:
        - A success message if payment is successfully executed and the database is updated.
        - Error messages for missing parameters or failure in executing the payment.
        """
        payment_id = request.query_params.get("paymentId")
        payer_id = request.query_params.get("PayerID")
        cart_id = request.query_params.get("cart_id")

        if not all([payment_id, payer_id, cart_id]):
            logger.error(f"Missing parameters: paymentId={payment_id}, payer_id={payer_id}, cart_id={cart_id}")
            return Response({"error": "Missing payment parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                db_payment = Payment.objects.get(paypal_payment_id=payment_id, order_id=cart_id)
                db_payment.status = "completed"
                db_payment.save()
                logger.info(f"Payment completed for cart_id={cart_id}, payment_id={payment_id}")
                return Response({"message": "Payment completed successfully"}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Payment execution failed: {payment.error}")
                return Response({"error": "Payment execution failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for payment_id={payment_id}, cart_id={cart_id}")
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            return Response({"error": "Payment processing failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentCancelView(APIView):
    """
    View to handle canceled PayPal payments.
    It marks the payment status as 'cancelled' in the database.
    """
    def get(self, request):
        """
        Handles the GET request for canceled payments.

        Parameters:
        - cart_id: The cart or order ID related to the canceled payment

        Returns:
        - A success message if payment is canceled successfully.
        - Error messages for missing parameters or failure in finding the pending payment.
        """
        cart_id = request.query_params.get("cart_id")

        if not cart_id:
            logger.error(f"Missing cart_id in cancel request")
            return Response({"error": "Missing cart_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            db_payment = Payment.objects.get(order_id=cart_id, status="pending")
            db_payment.status = "cancelled"
            db_payment.save()
            logger.info(f"Payment cancelled for cart_id={cart_id}")
            return Response({"message": "Payment cancelled successfully"}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            logger.error(f"Pending payment not found for cart_id={cart_id}")
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error cancelling payment: {str(e)}")
            return Response({"error": "Cancellation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
