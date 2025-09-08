from rest_framework import viewsets, permissions
from order.models import Order
from order.serializers.order_serializers import OrderSerializer
from product.permissions.custom import IsManagerOrReadOnly

class OrderPermission(permissions.BasePermission):
    """
    Permissão customizada:
    - POST: qualquer usuário autenticado pode criar.
    - PUT, PATCH, DELETE: apenas o dono do pedido ou staff pode modificar.
    - GET: qualquer usuário autenticado pode listar.
    """

    def has_permission(self, request, view):
        if request.method in ["POST", "GET"]:
            return request.user and request.user.is_authenticated
        # PUT, PATCH, DELETE: a checagem é feita no has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.user == request.user or request.user.is_staff
        return True

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def perform_create(self, serializer):
        # Garante que created_by e user sejam preenchidos automaticamente
        serializer.save(created_by=self.request.user, user=self.request.user)
