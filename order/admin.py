#agora não pode esquecer de realizar as migrações

from django.contrib import admin
from .models import Order

# Essa parte é para nós personalizarmos o order/admin.py.
# Próximo passo é fazer com o product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer_name','email', 'product_name','quantity','price', 'status']
    search_fields = ['customer_name','email','product_name']
    list_filter = ['status','created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ("Informações do cliente",{
            'fields' : ('customer_name','email')
        }),
        ("Detalhe do pedido",{
            'fields' : ('product_name','quantity','price','status')
        }),
        ("Data dos registros",{
            'fields': ('created_at','updated_at'),
            'classes': ('collapse',)
        })
    )


# Register your models here.
