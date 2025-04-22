import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema

from users.serializers.passwords import ResetPasswordSerializer

__all__ = ["ResetPasswordView"]

logger = logging.getLogger(__name__) 


class ResetPasswordView(APIView):
    """
    API view to handle password reset requests.
    
    This view accepts a POST request with a request body containing
    the data for password reset. If the data is valid, it performs
    the reset and returns a success message. Otherwise, it returns
    the validation errors.
    """
    
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        tags=["Password"]
    )
    def post(self, request) -> Response:
        """
        Handle the POST request to reset the password.
        
        Args:
            request (Request): The incoming HTTP request containing the password reset data.
        
        Returns:
            Response: A response indicating whether the password reset was successful or not.
        """
        logger.info("Password reset request received")  

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(
                f"Password reset successful for user: {user.email}"
            ) 

            return Response({
                "message": "Password reset successful."
            }, status=status.HTTP_200_OK)

        logger.warning(
            f"Password reset failed: {serializer.errors}"
        )

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )