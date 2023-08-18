from django.contrib import admin
from .models import CartItem

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart_id','quantity','category_size','category_color','user',)

admin.site.register(CartItem,CartItemAdmin)
