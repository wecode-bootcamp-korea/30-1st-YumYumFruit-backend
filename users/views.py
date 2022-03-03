import json
import bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models    import User
from users.validator import validate_email, validate_password

class SignupView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
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
                name         = name,
                email        = email,
                password     = decode_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message":"SUCCESS"},status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)