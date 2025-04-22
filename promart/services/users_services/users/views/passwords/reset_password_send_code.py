import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema

from users.serializers.passwords import ResetPasswordSendCodeSerializer

__all__ = ["ResetPasswordSendCodeView"]

logger = logging.getLogger(__name__) 


class ResetPasswordSendCodeView(APIView):
    """
    View to handle password reset requests by sending a reset code to the user's email.
    """

    @swagger_auto_schema(
        request_body=ResetPasswordSendCodeSerializer,
        tags=["Password"]
    )
    def post(self, request) -> Response:
        """
        Handle POST request to send a password reset code to the provided email.

        Args:
            request (Request): The request object containing the email for password reset.

        Returns:
            Response: A Response object containing the result of the password reset request.
        """
        logger.info(
            "Password reset request received for email: %s", 
            request.data.get("email")
        )

        serializer = ResetPasswordSendCodeSerializer(data=request.data)

        if serializer.is_valid():
            response_data = serializer.save()
            logger.info(
                "Password reset code sent successfully to email: %s", 
                request.data.get("email")
            )

            return Response(
                response_data, 
                status=status.HTTP_200_OK
            )

        logger.warning(
            "Password reset failed: %s", 
            serializer.errors
        )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )