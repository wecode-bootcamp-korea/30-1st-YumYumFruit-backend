import json

from django.http      import JsonResponse
from django.views     import View

from .models           import Product, ProductImage

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            images  = ProductImage.objects.filter(product_id=product_id)
            data = {
                    'product_id'          : product.id,
                    'name'                : product.name,
                    'country'             : product.country,
                    'price'               : product.price,
                    'thumbnail_image_url' : product.thumbnail_image_url,
                    'description'         : product.description,
                    'images'              : [
                        image.image_url
                     for image in images]
            }

            return JsonResponse({'data':data}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401) 