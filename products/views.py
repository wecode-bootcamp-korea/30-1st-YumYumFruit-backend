import math

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from products.models    import Product, ProductImage

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

class ProductListView(View):
    def get(self, request):
        try:
            sort        = request.GET.get("sort", "price")
            category_id = request.GET.get("category", "all")
            page        = int(request.GET.get("page", 1))
            page_size   = 12
            limit       = int(page_size * page)
            offset      = int(limit - page_size)

            category_validator = [1,2,3,4,"all"]

            if category_id not in category_validator:
                return JsonResponse({"results":"INVALID_PARAMETER"}, status=400)

            q = Q()
            if category_id != "all" :
                q &= Q(category_id=category_id)
                
            product_list   = Product.objects.filter(q)
            total_count    = product_list.count()
            page_count     = math.ceil(total_count / page_size)
            product_offset = list(product_list.order_by(sort)[offset:limit].values())

            return JsonResponse({
                "product_offset"       :product_offset,
                "total_number_of_pages":page_count,
                "total_count"          :total_count
                }, status=200)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)

