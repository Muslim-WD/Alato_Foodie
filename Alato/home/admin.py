from django.contrib import admin

from .models import FoodItem,Restaurant,Order,CartItem

# Register your model

admin.site.register(FoodItem)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(CartItem)
