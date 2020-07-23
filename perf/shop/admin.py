from django.contrib import admin

# Register your models here.
from .models import Product, Contact ,Orders, OrderUpdate      # Contact table for storing details of clients who have some query and asked through form

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)

