import logging
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from users.serializers import ChangePasswordSerializer

__all__ = ["ChangePasswordView"]

logger = logging.getLogger(__name__) 


class ChangePasswordView(APIView):
    """
    View for handling password change requests. The user must be authenticated to 
    access this endpoint.

    Methods:
        post: Accepts a POST request to change the user"s password. Validates and 
        updates the password.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        tags=["Password"]
    )
    def post(self, request) -> Response:
        """
        Handles the password change request for the authenticated user. If the 
        request is valid,
        the password is updated and a success message is returned. If invalid, 
        errors are returned.

        Args:
            request: The request object containing the current and new password.

        Returns:
            Response: A response with a message indicating success or failure.
        """
        logger.info(
            "Password change request received for user: %s", 
            request.user.email
        )

        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            logger.info(
                "Password changed successfully for user: %s", 
                request.user.email
            ) 
            return Response({
                "message": "Password changed successfully."
            }, status=status.HTTP_200_OK)
        
        logger.warning(
            "Password change failed for user: %s. Errors: %s", 
            request.user.email, 
            serializer.errors
        )  
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )