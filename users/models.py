from django.db import models

from products.models import Product

class User(models.Model):
    name         = models.CharField(max_length=30)
    email        = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    address      = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=50)
    point        = models.IntegerField(blank = True, null = True) 
    deposit      = models.IntegerField(blank = True, null = True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        
class ShoppingCart(models.Model):
    quantity   = models.IntegerField()
    user       = models.ForeignKey("User", on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shopping_carts'