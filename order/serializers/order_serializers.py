# o próximo passo é inserir os códigos no product/serializers/category_serializers.py
from itsdangerous import Serializer
from rest_framework import serializers
from order.models import Order

class OrderSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Order
        fields = "__all__"

