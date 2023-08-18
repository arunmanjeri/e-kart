from django.shortcuts import render,HttpResponse
from .models import Product,Category_type,Product_color,Product_size,ReviewRating,Variations
from django.db.models import Q
from django.core.paginator import Paginator

def store(request):
    product=Product.objects.all().order_by('-created_date')
    category=Category_type.objects.all()
    paginator=Paginator(product,6)
    page = request.GET.get('page')
    paged_product=paginator.get_page(page)
    context={
        'product':paged_product,
        'category':category,
    }
    return render(request,'store/store.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            category=Category_type.objects.all()
        context={
            'product':product,
            'category':category,
        }
        return render(request, 'store/store.html',context)
    return render(request, 'store/store.html')

def category_sort(request,type):
    product=Product.objects.filter(category_type__category_type=type).order_by('-created_date')
    category=Category_type.objects.all()
    context={
        'product':product,
        'category':category,
    }
    return render(request, 'store/store.html',context)

def product_view(request,prod_id):
    product=Product.objects.get(id=prod_id)
    if request.method == 'POST':
        rating=request.POST['rating']
        review=request.POST['review']
        if request.user.is_authenticated:
            data=ReviewRating(product_name=product, user=request.user, rating=rating, review=review)
            data.save()
        else:
            data=ReviewRating(product_name=product,rating=rating, review=review)
            data.save()
    datas=ReviewRating.objects.filter(product_name=product)
    data_count=datas.count()
    if data_count < 1:
        avg_rating=0
    else:
        sum=0
        for i in datas:
            sum += i.rating
            avg_rating=sum/data_count
    product_size=Product_size.objects.filter(product_name__id=prod_id)
    product_color=Product_color.objects.filter(product_name__id=prod_id)

    var=Variations.objects.filter(product_name=product)
    print(var.count())
    context={
        'product_size':product_size,
        'product_color':product_color,
        'product':product,
        'data':datas,
        'data_count':data_count,
        'avg_rating':avg_rating,
        'var':var,
    }
    return render(request, 'store/product_view.html',context)


