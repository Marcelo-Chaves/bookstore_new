from rest_framework import viewsets
from product.models.product import Product
from product.serializers.product_serializers import ProductSerializer
from product.permissions.custom import IsManagerOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrReadOnly]
