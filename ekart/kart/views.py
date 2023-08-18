from django.shortcuts import render,HttpResponse,redirect
from store.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required


def home(request):
    product=Product.objects.all().order_by('-created_date')
    context={
        'product':product,
    }
    return render(request,'index.html',context)

def cart_id_gen(request): 
    carting=request.session.session_key
    if not carting:
        carting=request.session.create()
    return carting


def add_to_cart(request,prod_id):
    if request.method == 'POST':
        color=request.POST['color']
        size=request.POST['size']
        product=Product.objects.get(id=prod_id)
        
        if request.user.is_authenticated:
            if CartItem.objects.filter(user=request.user).exists():
                if CartItem.objects.filter(product=product,category_size=size,category_color=color,user=request.user).exists():
                    obj=CartItem.objects.get(product=product,category_size=size,category_color=color,user=request.user)
                    obj.quantity+=1
                    obj.save()
                else:
                    carting=CartItem(user=request.user,cart_id=cart_id_gen(request),product=product,quantity=1,category_size=size,category_color=color)
                    carting.save()
            else:
                carting=CartItem(user=request.user,cart_id=cart_id_gen(request),product=product,quantity=1,category_size=size,category_color=color)
                carting.save()

        else:
            if CartItem.objects.filter(cart_id=cart_id_gen(request)).exists():
                if CartItem.objects.filter(cart_id=cart_id_gen(request),product=product,category_size=size,category_color=color).exists():
                    obj=CartItem.objects.get(cart_id=cart_id_gen(request),product=product,category_size=size,category_color=color)
                    obj.quantity+=1
                    obj.save()
                else:
                    carting=CartItem(cart_id=cart_id_gen(request),product=product,quantity=1,category_size=size,category_color=color)
                    carting.save()
            else:
                carting=CartItem(cart_id=cart_id_gen(request),product=product,quantity=1,category_size=size,category_color=color)
                carting.save()
    return redirect('cart_view')

def cart_view(request):
    if request.user.is_authenticated:
        if CartItem.objects.filter(user=request.user).exists():
            obj=CartItem.objects.filter(user=request.user)
            sum=0
            for i in obj:
                sum += (i.quantity * i.product.price)
            tax=sum*0.08
            grandtotal=tax+sum
        else:
            obj=None
            sum=0
            tax=0
            grandtotal=0
               
    else:
        if CartItem.objects.filter(cart_id=cart_id_gen(request)).exists():
            obj=CartItem.objects.filter(cart_id=cart_id_gen(request))
            sum=0
            for i in obj:
                sum += (i.quantity * i.product.price)
            tax=sum*0.08
            grandtotal=tax+sum
        else:
            obj=None
            sum=0
            tax=0
            grandtotal=0
    context={
        'product':obj,
        'total':sum,
        'tax':tax,
        'grand_total':grandtotal
    }        
    return render(request,'store/cart_view.html',context)

def cart_increase(request,item_id):
    obj=CartItem.objects.get(id=item_id)
    obj.quantity += 1
    obj.save()
    return redirect('cart_view')

def cart_decrease(request,item_id):
    obj=CartItem.objects.get(id=item_id)
    if obj.quantity <= 0:
        obj.delete()
    else:
        obj.quantity -= 1
        obj.save()
    return redirect('cart_view')

def item_remove(request,item_id):
    obj=CartItem.objects.get(id=item_id)
    obj.delete()
    return redirect('cart_view')


