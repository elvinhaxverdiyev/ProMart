import logging
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema

from users.serializers import LogoutSerializer

__all__ = ["LogoutView"]

logger = logging.getLogger(__name__)  


class LogoutView(APIView):
    """
    API view that handles user logout by blacklisting the provided refresh token.
    The refresh token is required for logging out the user and will be 
    invalidated upon successful logout.

    Methods:
        post: Logs the user out by blacklisting the provided refresh token.
    """

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        tags=["Users"]
    )
    def post(self, request) -> Response:
        """
        Handles the POST request to log the user out by blacklisting the refresh token.

        Args:
            request (Request): The HTTP request object containing the refresh token.

        Returns:
            Response: The response indicating the result of the logout operation.
        """
        logger.info("Logout request received")
        
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            logger.warning("No refresh token provided") 
            return Response({
                "detail": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info("User logged out successfully, token blacklisted") 
            return Response({
                "detail": "Successfully logged out."
            }, status=status.HTTP_200_OK)

        except TokenError:
            logger.error("Invalid token received: %s", refresh_token)  
            return Response({
                "detail": "Invalid token."
            }, status=status.HTTP_400_BAD_REQUEST)