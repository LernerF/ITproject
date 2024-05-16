from django.contrib import admin
from .models import Pizza, Cart, CartItem

admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItem)
