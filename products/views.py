import json, math

from django.http           import JsonResponse
from django.views          import View
from django.core.paginator import Paginator

from products.models    import Product, ProductImage, Category
from users.models       import User, ShoppingCart
from orders.models      import OrderDetail

class ProductListView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            sort     = data.get("sort", "-price")
            category = data.get("category", "1")

            product_list = list(Product.objects.filter(category_id=category).order_by(sort).values())
            # paginator    = Paginator(product_list, 12)
            # page = paginator.get_page(data.get("page", "1")) # paginator 사용해보고 싶어서 작업중이던 부분 일단 남겨둡니다

            return JsonResponse({"message":"SUCCESS", "results":results}, status=200)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"results":"INVALID_DATA"}, status=400)


    def get(self, request):
        try:
            sort     = request.GET.get("sort", "price") 
            category = request.GET.get("category", "all") 

            page      = int(request.GET.get("page", 1)) 
            page_size = 12
            limit     = int(page_size * page) 
            offset    = int(limit - page_size)

            if category != "all" :
                product_offset = list(Product.objects.filter(category_id=category).order_by(sort)[offset:limit].values())
                total_items    = Product.objects.filter(category_id=category).count()
            else:
                product_offset = list(Product.objects.all().order_by(sort)[offset:limit].values())
                total_items    = Product.objects.all().count()

            page_count     = math.ceil(total_items / page_size)
            return JsonResponse({"message":"SUCCESS", "results":product_offset, "total_pages":page_count, "total_items":total_items}, status=200)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"results":"INVALID_DATA"}, status=400)
