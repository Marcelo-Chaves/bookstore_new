# product/models/product.py
from django.utils import timezone
from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now) # só auto_now_add
    updated_at = models.DateTimeField(auto_now=True)      # só auto_now

    def __str__(self):
        return self.name
