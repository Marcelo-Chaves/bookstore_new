from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from order.models.order import Order
from order.serializers.order_serializers import OrderSerializer
from order.permissions.custom import IsManagerOrReadOnly

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
