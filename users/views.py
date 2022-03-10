import json
import bcrypt
import jwt

from django.http  import HttpResponseBadRequest, JsonResponse
from django.views import View
from datetime     import datetime, timedelta

from users.models    import User, ShoppingCart
from users.validator import validate_email, validate_password
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
            data = json.loads(request.body)
            packing_list = []

            for cart_recode in data:
                packing_list.append(cart_recode)
                user           = request.user
                product_id     = cart_recode['product_id']
                quantity       = cart_recode['quantity']
                packing_option = cart_recode['packing_option']

                if not Product.objects.filter(id=product_id).exists():
                    return JsonResponse({"message" : "PRODUCT_NOT_EXIST"}, status=400)
                
                if packing_option == "packaging":
                    packing_option = True
                else:
                    packing_option = False
                
                if quantity != 0:
                    ShoppingCart.objects.create(
                    user           = user,
                    product_id     = product_id,
                    quantity       = quantity,
                    packing_option = packing_option
                    )
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except ShoppingCart.DoesNotExist:
            return JsonResponse({"message" : "INVALID_CART"}, status=400)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
         
    @login_decorator     
    def get(self, request):

        user  = request.user
        carts = ShoppingCart.objects.select_related('product').filter(user_id=user) 
        
        if not ShoppingCart.objects.filter(user=user).exists():
            user_result = {
            'user_name' : user.name,
            'user_point': int(user.point)
        }
            return JsonResponse({"user_info" : user_result}, status=200)
        
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

        user  = request.user
        carts = request.GET.get('cart_id').split(',')

        for cart in carts:
            if cart == "0":
                ShoppingCart.objects.filter(user_id=user).delete()
                
                return JsonResponse({"message" : "ALL_DELETE_SUCCESS"}, status=204)
            
            if not ShoppingCart.objects.filter(id = cart, user = user).exists():
                return JsonResponse({"message" : "NOT_EXIST"}, status=400)
            
            ShoppingCart.objects.get(id = cart, user = user).delete()
            
        return JsonResponse({"message" : "DELETE_SUCCESS"}, status=204)
