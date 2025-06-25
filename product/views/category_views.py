#adicionar os códigos no product product/views/product_views.py
from rest_framework import viewsets
from product.models import Category
from product.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

