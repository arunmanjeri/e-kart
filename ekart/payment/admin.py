from django.contrib import admin
from .models import Order, OrderProduct,Payment


class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','fullname','phone','email','city','order_total','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','phone','email']
    list_per_page=15

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)