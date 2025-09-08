from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from product.models import Product  # relacionamento com produtos

class Order(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)  # valor padrão para evitar NULL
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} ({self.quantity})"
