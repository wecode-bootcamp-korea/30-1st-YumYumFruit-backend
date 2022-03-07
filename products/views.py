import json, math

from django.http           import JsonResponse
from django.views          import View

from products.models    import Product, ProductImage, Category
from users.models       import User, ShoppingCart
from orders.models      import OrderDetail

class ProductListView(View):
    def get(self, request):  
        try:
            sort      = request.GET.get("sort", "price")
            category  = request.GET.get("category", "all")
            page      = int(request.GET.get("page", 1))
            page_size = 12
            limit     = int(page_size * page)
            offset    = int(limit - page_size)

            if category != "all" :
                product_list   = Product.objects.filter(category_id=category)
            else:
                product_list   = Product.objects.all()

            total_items    = product_list.count()
            page_count     = math.ceil(total_items / page_size)
            product_offset = list(product_list.order_by(sort)[offset:limit].values())

            return JsonResponse({
                                    "message"    :"SUCCESS",
                                    "results"    :product_offset,
                                    "total_pages":page_count,
                                    "total_items":total_items
                                }, status=200)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"results":"INVALID_DATA"}, status=400)
        except ValueError:
            return JsonResponse({"results":"INVALID_PARAMETER"}, status=400)
