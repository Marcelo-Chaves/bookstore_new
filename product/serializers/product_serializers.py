#agora temos que acrescentar o código no __init__.py (order/serializers/__init__.py) e no
from rest_framework import serializers
from product.models import Product, Category
from product.serializers.category_serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"


