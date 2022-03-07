import json
import bcrypt
import jwt

from django.http  import HttpResponseBadRequest, JsonResponse
from django.views import View
from datetime     import datetime, timedelta

from users.models    import User, ShoppingCart
from users.validator import validate_email, validate_password
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

