from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404


from users.models import CustomUser
from users.serializers import CustomUserSerializer
class UserListView(APIView):

    @swagger_auto_schema(
        operation_description="Bütün istifadəçilərin siyahısını gətirir (yalnız adminlər üçün).",
        responses={200: CustomUserSerializer(many=True)},
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):

    @swagger_auto_schema(
        operation_description="İstifadəçinin detalları (id ilə).",
        responses={200: CustomUserSerializer()},
    )
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)