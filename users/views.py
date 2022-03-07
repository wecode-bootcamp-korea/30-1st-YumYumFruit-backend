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