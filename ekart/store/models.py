from django.db import models
from accounts.models import Account

class Category_type(models.Model):
    category_type=models.CharField(max_length=20)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_type

class Product(models.Model):
    product_name=models.CharField(max_length=200, unique=False)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products',blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category_type=models.ForeignKey(Category_type, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.product_name
    
class Product_color(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    category_color=models.CharField(max_length=20)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product_name

class Product_size(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    category_size=models.CharField(max_length=20)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product_name

class ReviewRating(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    rating=models.IntegerField(default=1)
    review=models.TextField(max_length=500,blank=True)

    def __unicode__(self):
        return self.product_name

class Variations(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    images=models.ImageField(upload_to='photos/variation',blank=True)

    def __unicode__(self):
        return self.product_name