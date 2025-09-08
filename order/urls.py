# order/urls.py
from rest_framework import routers
from order.views.order_views import OrderViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")  # o router gerencia "orders/"

urlpatterns = [
    path("", include(router.urls)),  # inclui todas as rotas do router
]
