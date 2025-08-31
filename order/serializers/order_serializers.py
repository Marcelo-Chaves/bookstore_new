from rest_framework import serializers
from order.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "name", "description", "created_by", "created_at", "updated_at"]
        read_only_fields = ["created_by", "created_at", "updated_at"]
