from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from store.models import Product
from .models import Whishlist

def whishlist_id_gen(request): 
    list_id=request.session.session_key
    if not list_id:
        list_id=request.session.create()
    return list_id

def add_to_whishlist(request,prod_id):
    if request.user.is_authenticated:
        if Whishlist.objects.filter(product_id=prod_id,user=request.user).exists():
            pass
        else:
            whishlist=Whishlist(user=request.user,product_id=prod_id,whishlist_id=whishlist_id_gen(request))
            whishlist.save()
    else:
        if Whishlist.objects.filter(product_id=prod_id,whishlist_id=whishlist_id_gen(request)).exists():
            pass
        else:
            whishlist=Whishlist(product_id=prod_id,whishlist_id=whishlist_id_gen(request))
            whishlist.save()
    try:
        referer_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url)
    except:
        return redirect('store')
    
def whishlist_view(request):
    if request.user.is_authenticated:
        if Whishlist.objects.filter(user=request.user).exists():
            obj=Whishlist.objects.filter(user=request.user)
        else:
            obj=None
            
    else:
        if Whishlist.objects.filter(whishlist_id=whishlist_id_gen(request)).exists():
            obj=Whishlist.objects.filter(whishlist_id=whishlist_id_gen(request))
        else:
            obj=None
            
    context={
        'product':obj,
    }
                
    return render(request,'store/whishlist.html',context)


def witem_remove(request,item_id):
    obj=Whishlist.objects.get(id=item_id)
    obj.delete()
    return redirect('whishlist_view')