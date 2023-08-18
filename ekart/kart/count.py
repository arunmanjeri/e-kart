from .models import CartItem
from .views import cart_id_gen
from whishlist.views import whishlist_id_gen
from whishlist.models import Whishlist

def counter(request):
    carting_count=0
    if 'admin' in request.path:
        return {}

    else:
        try:
            if request.user.is_authenticated:
                obj=CartItem.objects.filter(user=request.user)
                for i in obj:
                    carting_count=carting_count+i.quantity 
            else:
                obj=CartItem.objects.filter(cart_id=cart_id_gen(request))
                for i in obj:
                    carting_count=carting_count+i.quantity
        except CartItem.DoesNotExist:
            carting_count = 0
    return dict(cart_count=carting_count)

def wcounter(request):
    whishlist_count=0
    if 'admin' in request.path:
        return {}

    else:
        try:
            if request.user.is_authenticated:
                obj=Whishlist.objects.filter(user=request.user)
                whishlist_count=obj.count()
            else:
                obj=Whishlist.objects.filter(whishlist_id=cart_id_gen(request))
                whishlist_count=obj.count()
        except Whishlist.DoesNotExist:
            whishlist_count = 0
    return dict(whishlist_count=whishlist_count)