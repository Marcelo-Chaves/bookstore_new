from ipaddress import collapse_addresses

from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    list_display = ['is_active', 'category', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at','updated_at']

    fieldsets = (
        ("informações básicas",{
            'fields':('name','description','category')
        }),
        ("Detalhes de estoque e preço", {
            'fields' : ('price', 'stock', 'is_active')
        }),
        ("Datas de registros",{
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })

    )
# Register your models here.
