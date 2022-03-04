import os, django, csv 

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yumyumfruits.settings")
django.setup()

from orders.models     import Order, OrderDetail
from products.models   import Product, ProductImage, Category
from users.models      import ShoppingCart

        

CSV_PATH_PRODUCTS = "./csv/products.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if not Category.objects.filter(name=row[0]).exists():
            Category.objects.create(
				name = row[0]
            )

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            name                = row[1],
            country             = row[2],
            price               = row[3],
            receiving_date      = row[4],
            description         = row[5],
            thumbnail_image_url = row[6],
            category            = Category.objects.get(name = row[0])
        )


CSV_PATH_PRODUCTS = "./csv/orders.csv"
 
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
            Order.objects.create(
                total_price  = row[0],
                shipping_fee = row[1],
                paid_point   = row[2],
                paid_deposit = row[3],
                user_id      = row[4],
            ) 

CSV_PATH_PRODUCTS = "./csv/detail.csv"
 
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
            OrderDetail.objects.create(
                quantity      = row[0],
                earned_point  = row[1],
                product_price = row[2],
                order_id      = row[3],
                product_id    = row[4]
        ) 

CSV_PATH_PRODUCTS = "./csv/product_images.csv"
 
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    temp = ""
    for row in data_reader:
        if row[2]:
            product_id = row[2]
        
        ProductImage.objects.create(
            product_id = product_id,
            image_url  = row[3]
        )

CSV_PATH_PRODUCTS = "./csv/shopping_carts.csv"
 
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
            ShoppingCart.objects.create(
                user_id    = row[0],
                product_id = row[1],
                quantity   = row[2]
        ) 

