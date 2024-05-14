from django.contrib import admin
from .models import Pizza, Cart, CartItem, Ingredient

admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Ingredient)