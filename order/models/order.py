# não pode esquecer de importar no order/models/__init__.py (from .order import Order)
from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
        ],
        default="pending"
    )

    def __str__(self):
        return f"{self.customer_name} - {self.product_name} ({self.quantity})"