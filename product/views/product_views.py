#product/views/product_views.py
from rest_framework import viewsets, permissions
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permissão para Product e Category:
    - GET (listar e visualizar): acesso público (sem autenticação)
    - POST, PUT, PATCH, DELETE: apenas usuários staff
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
