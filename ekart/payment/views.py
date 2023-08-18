from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime
from kart.models import CartItem
from kart.views import cart_id_gen
from store.models import Product
import random
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='login_user')
def checkout(request):
    current_user=request.user
    carting_items=CartItem.objects.filter(user=current_user)
    carting_count=carting_items.count()
    if carting_count<=0:
        return redirect('store')
    grand_total=0
    tax=0
    total=0
    quantity=0
    for carting_item in carting_items:
        total=total+(carting_item.product.price*carting_item.quantity)
        quantity=quantity+carting_item.quantity
    tax=(8*total)/100
    grand_total=total+tax

    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.tax=tax
            data.order_total=grand_total
            data.save()

            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d')
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'carting_items':carting_items,
                'total':total,
                'tax':tax,
                'grandtotal':grand_total
            }
            return render(request,'payment/payments.html',context)
        else:
            return redirect('checkout')
    form=OrderForm()

    try:
        total=0
        tax=0
        grandtotal=0
        quantity=0
        current_user=request.user
        if current_user.is_authenticated:
            carting_items=CartItem.objects.filter(user=current_user, is_active=True)

        for carting_item in carting_items:
            total+=((carting_item.product.price)*(carting_item.quantity))
            quantity+=carting_item.quantity
        tax=(total*8)/100
        grandtotal=total+tax
    except:
        pass
    context={
        'form':form,
        'total':total,
        'tax':tax,
        'grandtotal':grandtotal,
        'quantity':quantity,
        'carting_items':carting_items
    }
    return render(request,'payment/checkout.html',context)

@login_required(login_url='login_user')
def payments(request):
    body=json.loads(request.body)
    order_number=body['orderId']
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
    order.status='Completed'
    order.save()
    payment=Payment(
        user=request.user,
        payment_id=body['transId'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status']
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    #move cartitems to ordered product
    carting_items=CartItem.objects.filter(user=request.user)

    for item in carting_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product.id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        carting_item=CartItem.objects.get(id=item.id)
        category_size=carting_item.category_size
        category_color=carting_item.category_color
        order_product=OrderProduct.objects.get(id=orderproduct.id)
        order_product.category_size=category_size
        order_product.category_color=category_color
        order_product.save()

        #reduce quantity of product
        product=Product.objects.get(id=item.product_id)
        product.stock = product.stock-item.quantity
        product.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()

    # send order recieve email to customer
    try:
        user=request.user
        mail_subject='Welcome Ekart, Order Placed'
        message='Hi '+user.first_name+user.last_name+' Successfully placed your order, order id :'+order_number+', Please ignore this message, if it is not you!'
        to_email=user.email
        send_mail=EmailMessage(mail_subject,message,to=[to_email])
        send_mail.send()
    except:
        pass
    data={
        'order_number':order.order_number,
        'transId':payment.payment_id,
    }
    print(data['order_number'])
    print(data['transId'])
    return JsonResponse(data)

def order_complete(request):
    order_number=request.GET.get('order_number')
    transid=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=OrderProduct.objects.filter(order_id=order.id)
        payment=Payment.objects.get(payment_id=transid)

        subtotal=0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transid':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'payment/order_complete.html',context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')