from rest_framework.views import APIView, status, Response
from django.shortcuts import get_object_or_404

from products.models import Category
from products.serializers import CategorySerializer, SubCategorySerializer



__all__ = [
    "SuperCategoryAPIView",
    "SubCategoryAPIView"
]

class SuperCategoryAPIView(APIView):
    def get(self, request):
        categies = Category.objects.filter(super_category__isnull=True)
        serializer = CategorySerializer(categies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SubCategoryAPIView(APIView):
    def get(self, request, super_id):
        super_category = get_object_or_404(Category, id=super_id)
        sub_categories = Category.objects.filter(super_category=super_category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
