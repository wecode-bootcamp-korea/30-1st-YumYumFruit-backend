import json, math

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from products.models    import Product, ProductImage, Category
from users.models       import User, ShoppingCart
from orders.models      import OrderDetail

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
