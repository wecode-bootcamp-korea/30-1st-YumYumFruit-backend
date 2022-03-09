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

class WishlistView(View):
    @login_decorator
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user  
            wish_product = data["product_id"]
        
            if Wishlist.objects.filter(user_id=user.id,product_id=wish_product).exists():
              return JsonResponse({"message" : "DUPLICATE_PRODUCT"})
            else:
                Wishlist.objects.create(user_id=user.id,product_id=wish_product)
                return JsonResponse({"message" : "WISHLIST_CREATED"},status=201)
        
        except Wishlist.DoesNotExist:
            return JsonResponse({"message" : "INVALID_CART"}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
   
    @login_decorator   
    def get(self,request):
        try:
            user      = request.user
            wishlists = Wishlist.objects.filter(user_id=user.id)
              
            result = [
                {
                    'user_id'                 : user.id,
                    'product_id'              : wishlist.product.id,
                    'name'                    : wishlist.product.name,
                    'price'                   : int(wishlist.product.price),
                    'thumbnail_image_url'     : wishlist.product.thumbnail_image_url,
                } for wishlist in wishlists
            ]
            return JsonResponse({"result":result},status=200)
            
        except Wishlist.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXITST_WISHLIST'}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    # @login_decorator
    # def delete(self,request,product_id):
    #     try:
    #         user = request.user  
    #         Wishlist.objects.filter(user_id=user.id,product_id=product_id).delete()
            
    #         return JsonResponse({'result':'DELETE_SELECT PRODUCT'}, status = 200)
        
    #     except KeyError:
    #          return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    @login_decorator
    def delete(self,request):
        try:
            user     = request.user 
            wishlists = request.GET.get("wishlist_id").split(",")
            
            for wishlist in wishlists:
                
                if wishlist == "0":
                    Wishlist.objects.filter(user_id=user.id).all().delete()
                   
                
                Wishlist.objects.filter(user_id=user.id,id=wishlist).delete()
            
            return JsonResponse({"message":"DELETE_SUCCESS"},status=204)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    