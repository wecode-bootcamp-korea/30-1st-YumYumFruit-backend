import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from users.models    import User, ShoppingCart
from users.validator import validate_email, validate_password
from my_settings  import SECRET_KEY, AIGORHM
from users.utils import login_decorator
from products.models import Product

class SignupView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            username       = data['username']
            email          = data['email']
            password       = data['password']
            phone_number   = data['phone_number']   
            
            if not validate_email(email):
                   return JsonResponse({"message" : "INVAILD EMAIL"}, status = 400)
            
            if not validate_password(password):
                       return JsonResponse({"message" : "INVALID PASSWORD"}, status = 400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message":"DUPLICATE_EMAIL"}, status=400)
            
            new_salt = bcrypt.gensalt()
            new_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(new_password,new_salt) 
            decode_password = hashed_password.decode('utf-8')
             
            User.objects.create(
                name         = username,
                email        = email,
                password     = decode_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message":"SUCCESS"},status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

class SigninView(View):
      def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
                    
            if not User.objects.filter(email = email).exists():
                return JsonResponse({"message":"INVALID_USER"},status=401)
            
            user            = User.objects.get(email=email)
            hashed_password = user.password.encode('utf-8') 
          
            if bcrypt.checkpw(password.encode('utf-8'),hashed_password):
                token = jwt.encode({'id': user.id},SECRET_KEY,AIGORHM)
                return JsonResponse({"token":token},status=200)
            
            return JsonResponse({"message": "INVAILD_USER"}, status=401)  
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400) 
        
class ShoppingCartView(View):
    @login_decorator
    def post(self,request):
        try:
            data       = json.loader(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']
        
            cart, created = ShoppingCart.objects.get_or_create(
                user_id    =  user,
                quantity   = quantity,
                product_id = product_id 
            )          
            
            if not created:
                cart.quantity += quantity,
                cart.save() 
            
            current_cart = ShoppingCart.objects.filter(user_id = request.user_id).count()
            
            success_message = {
                'result' : {
                    'message' : 'SUCCESS',
                    'current_total_cart': current_cart
                }
            }
            return JsonResponse(success_message, status = 200)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : "USER_ID_DOES_NOT_EXIST"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"KET_ERROR"},status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : "JSON_DECODE_ERROR"}, status = 400) 

    @login_decorator
    def get(self,request):
        user  = request.user.id
        carts = ShoppingCart.objects.filter(user=user)
        count = carts.count()
        
        result = [
            {
                'name'                : cart.product.name,
                'price'               : cart.product.price,
                'thumbnail_image_url' : cart.product.image_set.all()[0].img_url,
                'description'         : cart.Product.description,
            } for cart in carts ]

        return JsonResponse({
            'result' : result,
            'count'  : count
        }, status = 200)
    
    @login_decorator
    def patch (self, request):
        try:
            data = json.loads(request.body)
            cart = ShoppingCart.objects.get(id = data['cart_id'])
            cart.quantity = data['quantity']
            cart.save()

            current_cart = ShoppingCart.objects.filter(user_id = request.user.id).count()
            success_message = {
                'result' : {
                    'message' : 'SUCCESS',
                    'current_total_cart': current_cart
                }
            }
            return JsonResponse(success_message, status = 200)

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : "JSON_DECODE_ERROR"}, status = 400)
    
    
    
    @login_decorator
    def delete (self,request):
        try:
            cart_ids = request.GET.getlist('cart_id',None)
            carts    = ShoppingCart.objects.filter(id=cart_ids)
            
            if not carts:
                return JsonResponse({"message":'CART_NOT_EXIST'})
            
            carts.delete()
            
            current_cart = ShoppingCart.objects.filter(user_id = request.user.id).count()
            success_message = {
                'result' : {
                    'message' : 'SUCCESS',
                    'current_total_cart': current_cart
                }
            }
            return JsonResponse(success_message, status = 200)

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)      
        except ShoppingCart.DoesNotExist:
            return JsonResponse({'message' : "CART_NOT_EXIST"}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : "JSON_DECODE_ERROR"}, status = 400)
            