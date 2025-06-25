# Próximo passo é inserir os códigos no product/serializers/product_serializers.py
from rest_framework import serializers
from product.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        modo = Category
        fields = "__all__"