from rest_framework.permissions import BasePermission

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True  # leitura liberada para todos
        return request.user and request.user.is_staff  # escrita só para staff
