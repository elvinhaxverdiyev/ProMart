import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import CustomUser
from users.serializers import CustomUserSerializer

logger = logging.getLogger(__name__)

__all__ = [
    "UserListView",
    "UserDetailView"
]


class UserListView(APIView):
    """
    API view to retrieve the list of all users.
    Only accessible by admin users.
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve the list of all users. (Admin only)",
        responses={200: CustomUserSerializer(many=True)},
        tags=["Users"]
    )
    def get(self, request):
        logger.info("Admin %s requested user list.", request.user.email)
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    API view to retrieve the details of a specific user by ID.
    Only accessible by admin users.
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve user details by ID. (Admin only)",
        responses={200: CustomUserSerializer()},
        manual_parameters=[
            openapi.Parameter(
                "user_id", 
                openapi.IN_PATH, 
                description="ID of the user", 
                type=openapi.TYPE_INTEGER
            )
        ],
        tags=["Users"]
    )
    def get(self, request, user_id):
        logger.info("Admin %s requested details for user ID %s.", request.user.email, user_id)
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
