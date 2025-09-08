# order/permissions/custom.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        # POST permitido para qualquer usuário autenticado
        if request.method == "POST" and request.user and request.user.is_authenticated:
            return True
        # PUT, DELETE apenas para staff
        return request.user and request.user.is_staff
