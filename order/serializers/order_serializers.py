# order/serializers/order_serializers.py
from rest_framework import serializers
from order.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "description",
            "product",
            "quantity",
            "user",
            "created_by",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["user", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        validated_data["user"] = request_user
        validated_data["created_by"] = request_user
        return super().create(validated_data)
