import json
import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, AIGORHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')          
            payload = jwt.decode(token, SECRET_KEY, AIGORHM)  
            user = User.objects.get(id=payload['id'])                 
            request.user = user                                                

        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:                                           
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper