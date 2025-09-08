from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp na criação
    updated_at = models.DateTimeField(auto_now=True)      # timestamp na atualização

    def __str__(self):
        return self.name
