from django.contrib import admin
from .models import Category_type,Product,Product_color,Product_size,ReviewRating,Variations

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','category_type','is_available','stock','price',)
    list_filter=('category_type','product_name')


class ColorAdmin(admin.ModelAdmin):
    list_display=('product_name','category_color',)

class SizeAdmin(admin.ModelAdmin):
    list_display=('product_name','category_size',)


class DataAdmin(admin.ModelAdmin):
    list_display=('product_name','rating','user',)

class VarAdmin(admin.ModelAdmin):
    list_display=('product_name',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Category_type)
admin.site.register(Product_size,SizeAdmin)
admin.site.register(Product_color,ColorAdmin)
admin.site.register(ReviewRating,DataAdmin)
admin.site.register(Variations,VarAdmin)