import json

import bcrypt
import jwt

from django.http  import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from datetime     import datetime, timedelta

from users.models    import User, Wishlist
from users.validator import validate_email, validate_password
from users.utils     import login_decorator
from my_settings     import SECRET_KEY, ALGORITHM
from users.utils     import login_decorator
from products.models import Product

class SignupView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            phone_number   = data['phone_number']   
            
            if not validate_email(email):
                return JsonResponse({"message" : "INVAILD_EMAIL"}, status = 400)
            
            if not validate_password(password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "DUPLICATE_EMAIL"}, status=400)
            
            new_salt = bcrypt.gensalt()
            new_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(new_password,new_salt) 
            decode_password = hashed_password.decode('utf-8')
             
            User.objects.create(
                name         = name,
                email        = email,
                password     = decode_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message" : "SUCCESS"},status=201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status=400)

class SigninView(View):
      def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
                    
            if not User.objects.filter(email=email).exists():
              return HttpResponseBadRequest(status=404)
            
            user            = User.objects.get(email=email)
            hashed_password = user.password.encode('utf-8') 
            
            if not bcrypt.checkpw(password.encode('utf-8'),hashed_password):
                return JsonResponse({"message" : "INVAILD_USER"}, status=401) 
            
            token = jwt.encode({'id': user.id, 'exp':datetime.utcnow() + timedelta(days=2)},SECRET_KEY,ALGORITHM)
            
       
            return JsonResponse({"token" : token},status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400) 

          
class ShoppingCartView(View):
    @login_decorator
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            product_id      = data['product_id']
            packing_options = data['packing_options']
            
            for packing_option in packing_options[::]:
                if packing_option['quantity'] == 0:
                    packing_options.remove(packing_option)
                    
            if len(packing_options) == 0:
                return JsonResponse({"message" : "INVAILD_ITEM"}, status=400)
            
            cart_instance = [ShoppingCart(
                user           = user,
                product_id     = product_id,
                quantity       = cart_item["quantity"],
                packing_option = cart_item["packing_option"]
            ) for cart_item in packing_options if cart_item["quantity"] != 0]
            
            ShoppingCart.objects.bulk_create(cart_instance)
               
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
         
    @login_decorator     
    def get(self, request):

        user        = request.user
        carts       = ShoppingCart.objects.filter(user_id=user.id) 
        user_result = {
            'user_name'  : user.name,
            'user_points': int(user.point)
        }
        
        cart_result = [{
            'cart_id'             : cart.id,
            'product_id'          : cart.product.id,
            'name'                : cart.product.name,
            'price'               : int(cart.product.price),
            'thumbnail_image_url' : cart.product.thumbnail_image_url,
            'quantity'            : cart.quantity,
            'packing_option'      : cart.packing_option
        } for cart in carts ]
            
        return JsonResponse({"user_info": user_result,"cart_info" : cart_result}, status=200)


    @login_decorator
    def patch(self, request):
        try:
            user     = request.user
            data     = json.loads(request.body)
            cart_id  = data['cart_id']
            quantity = data['quantity']
            
            if not ShoppingCart.objects.filter(id=cart_id, user_id=user.id).exists():
                return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)
            
            cart = ShoppingCart.objects.get(id=cart_id, user_id=user.id)

            cart.quantity = quantity
            cart.save()

            if cart.quantity <= 0:
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
    
    @login_decorator
    def delete(self, request):
        try:
            user  = request.user
            cart_delete =  request.GET.get('cart_id')
            
            if cart_delete == "all":
                ShoppingCart.objects.filter(user_id=user.id).delete()
                
                return JsonResponse({"message" : "ALL_DELETE_SUCCESS"}, status=204)
            
            carts = request.GET.get('cart_id').split(',')

            if ShoppingCart.objects.filter(id__in=carts, user_id=user.id):
                ShoppingCart.objects.filter(id__in=carts, user_id=user.id).delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"}, status=204)
            else:
                return JsonResponse({"message" : "INVAILD_CART"}, status=400)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class WishlistView(View):
    @login_decorator
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user  
            wish_product = data["product_id"]
        
            if Wishlist.objects.filter(user_id=user.id,product_id=wish_product).exists():
                return JsonResponse({"message" : "DUPLICATE_PRODUCT"},status=400)
            
            Wishlist.objects.create(user_id=user.id,product_id=wish_product)
            
            return JsonResponse({"message" : "WISHLIST_CREATED"},status=201)
        except Wishlist.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_WISHLIST'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
   
    @login_decorator   
    def get(self,request):
        try:
            user      = request.user
            wishlists = Wishlist.objects.filter(user_id=user.id)
              
            result = [
                {
                    'user_id'             : user.id,
                    'product_id'          : wishlist.product.id,
                    'name'                : wishlist.product.name,
                    'price'               : int(wishlist.product.price),
                    'thumbnail_image_url' : wishlist.product.thumbnail_image_url,
                } for wishlist in wishlists
            ]
            return JsonResponse({"result" : result},status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)    
   
    @login_decorator
    def delete(self,request):
        try:
            user      = request.user 
            wishlists = request.GET.get("wishlist_id").split(",")
            wishlist_all  = request.GET.get("wishlist_id")
            
            if wishlist_all == "all":
                Wishlist.objects.filter(user_id=user.id).delete()
                return JsonResponse({"message": "ALL_DELETE_SUCCESS"},status=204)
           
            if Wishlist.objects.filter(user_id=user.id,id__in=wishlists).exists():
                Wishlist.objects.filter(user_id=user.id,id__in=wishlists).delete()
                return JsonResponse({"message": "DELETE_SUCCESS"},status=204)
            else:
                 return JsonResponse({'message' : 'DOES_NOT_REQUEST_PRODUCT'}, status = 400)    
             
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)