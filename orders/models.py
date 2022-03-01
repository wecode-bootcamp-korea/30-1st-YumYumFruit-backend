from django.db import models

from users.models    import User
from products.models import Product


class Order(models.Model):
    total_price  = models.DecimalField(decimal_places=2, max_digits = 20)
    shipping_fee = models.DecimalField(decimal_places=2, max_digits = 20)
    paid_point   = models.DecimalField(decimal_places=2, max_digits = 20)
    paid_deposit = models.DecimalField(decimal_places=2, max_digits = 20)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'
        
        
class OrderDetail(models.Model):
    quantity      = models.IntegerField()
    earned_point  = models.DecimalField(decimal_places=2, max_digits = 20)
    product_price = models.DecimalField(decimal_places=2, max_digits = 20)
    order         = models.ForeignKey(Order, on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_details'