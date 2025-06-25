#agora não pode esquecer de realizar as migrações ( makemigrations e migrate)

from django.contrib import admin
from .models import Order

admin.site.register(Order)

# Register your models here.
