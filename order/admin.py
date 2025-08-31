from django.contrib import admin
from order.models.order import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_by", "created_at", "updated_at"]
    readonly_fields = ["created_by", "created_at", "updated_at"]
