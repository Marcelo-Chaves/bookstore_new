#agora é para colocar no product/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order.views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet,basename='Order')

urlpatterns =[
    path('', include(router.urls))
]