from rest_framework import viewsets, permissions
from order.models import Order
from order.serializers.order_serializers import OrderSerializer

class OrderPermission(permissions.BasePermission):
    """
    Permissão para Orders:
    - GET/POST/PUT/DELETE: apenas usuários autenticados
    - PUT/PATCH/DELETE: apenas dono ou staff
    """

    def has_permission(self, request, view):
        # Apenas usuários autenticados podem acessar qualquer ação
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Dono ou staff podem alterar/deletar
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.user == request.user or request.user.is_staff
        return True


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, user=self.request.user)

