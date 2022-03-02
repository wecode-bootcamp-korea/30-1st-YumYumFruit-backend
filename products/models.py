from django.db import models

class Product(models.Model):
    name                = models.CharField(max_length=30)
    country             = models.CharField(max_length=30)
    price               = models.DecimalField(decimal_places=2, max_digits = 20)
    receiving_date      = models.DateTimeField(auto_now_add=True)
    description         = models.CharField(max_length=200)
    thumbnail_image_url = models.CharField(max_length=200)
    category            = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        
        
class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'categories'
        

class ProductImage(models.Model):
    image_url = models.CharField(max_length=200)
    product   = models.ForeignKey("Product", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_images'