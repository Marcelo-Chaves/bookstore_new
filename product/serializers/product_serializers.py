from rest_framework import serializers
from product.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
