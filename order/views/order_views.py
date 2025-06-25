#agora acrescentar os código no product/views/category_views.py
from rest_framework import viewsets
from order.models import Order
from order.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


