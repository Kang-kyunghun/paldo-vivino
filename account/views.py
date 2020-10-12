import json
import bcrypt
import jwt

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from paldo.settings     import SECRET_KEY, ALGORITHM
from .models            import Account, Wishlist

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            PASSWORD_LENGTH = 8
            
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'DUPLICATED_EMAIL'}, status=400)
            
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'NOT INCLUDE @ or . '}, status= 400)
            
            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({'message':'PASSWORD TOO SHORT'}, status= 400)
            
            password         = data['password']
            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            Account.objects.create(
                email        = data['email'],
                first_name   = data['first_name'],
                last_name    = data['last_name'],
                password     = hashed_password
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)