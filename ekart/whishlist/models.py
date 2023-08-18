from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.

class Whishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    whishlist_id=models.CharField(max_length=50, null=True)
    is_active=models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
