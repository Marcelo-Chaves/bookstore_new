from rest_framework.permissions import BasePermission

class IsManagerOrReadOnly(BasePermission):
    """
    Permite leitura para todos, mas escrita apenas para usuários staff/manager.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
