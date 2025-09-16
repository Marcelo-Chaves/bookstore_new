# product/views/category_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models.category import Category
from product.serializers.category_serializers import CategorySerializer
from product.permissions.custom import IsManagerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ IsManagerOrReadOnly]
