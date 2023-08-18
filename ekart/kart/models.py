from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.

class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id=models.CharField(max_length=50, null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    category_size=models.CharField(max_length=20)
    category_color=models.CharField(max_length=20)

    def __unicode__(self):
        return self.product
    
    def subtotal(self):
        sub=self.quantity*self.product.price
        return sub