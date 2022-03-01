from django.db import models

from users.models import User
from products.models import Product


class Order(models.Model):
    total_price  = models.IntegerField()
    shipping_fee = models.IntegerField()
    paid_point   = models.IntegerField()
    paid_deposit = models.IntegerField()
    user         = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'
        
        
class OrderDetail(models.Model):
    quantity      = models.IntegerField()
    earned_point  = models.IntegerField()
    product_price = models.IntegerField()
    order         = models.ForeignKey(Order, on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_details'