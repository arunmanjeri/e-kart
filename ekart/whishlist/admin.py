from django.contrib import admin
from .models import Whishlist


class WhishlistAdmin(admin.ModelAdmin):
    list_display=('product','whishlist_id','user',)

admin.site.register(Whishlist,WhishlistAdmin)
