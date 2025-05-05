from rest_framework.views import APIView, status, Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from products.models import Category
from products.serializers import CategorySerializer, SubCategorySerializer

__all__ = [
    "SuperCategoryAPIView",
    "SubCategoryAPIView"
]


class SuperCategoryAPIView(APIView):
    """
    API endpoint for listing all super categories.
    
    This view returns all categories that do not have a parent category, i.e., super categories.
    """
    @swagger_auto_schema(
        operation_description="Retrieve all super categories that do not have a parent category.",
        tags=["Categories"],
        responses={status.HTTP_200_OK: CategorySerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieves and returns a list of all super categories.
        
        A super category is a category that does not have a parent category.
        This method is accessible by anyone.
        """
        categories = Category.objects.filter(super_category__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryAPIView(APIView):
    """
    API endpoint for listing all sub-categories under a specific super category.
    
    This view returns all sub-categories associated with a given super category, identified by its ID.
    """
    @swagger_auto_schema(
        operation_description="Retrieve all sub-categories under a specific super category identified by its ID.",
        tags=["Categories"],
        responses={status.HTTP_200_OK: SubCategorySerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "super_id", 
                openapi.IN_PATH, 
                description="ID of the super category", 
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, super_id):
        """
        Retrieves and returns a list of sub-categories under the specified super category.
        
        This method requires a valid super category ID to fetch the sub-categories.
        """
        super_category = get_object_or_404(Category, id=super_id)
        sub_categories = Category.objects.filter(super_category=super_category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)