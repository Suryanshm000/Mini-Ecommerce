from django.contrib import admin
from .models import CustomUser, Vendor, Product, CartItem, Order

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)

