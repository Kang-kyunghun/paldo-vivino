import json 
import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from paldo.settings         import SECRET_KEY, ALGORITHM
from account.models         import WishList


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.headers.get('Authorization'): 
            return JsonResponse({'message':'NO_TOKEN'}, status=403)
        token = request.headers['Authorization']

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
            request.user_id = decoded_token['user_id']
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=403)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=403)

        return func(self, request, *args, **kwargs) 
    return wrapper

def check_wishlist(request, id):
    if not request.headers.get('Authorization'):
        return False
    token = request.headers['Authorization']

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        if WishList.objects.filter(user_id=decoded_token['user_id']).filter(vintage_id = id).exists():
            return True
        else:
            return False
    
    except jwt.exceptions.DecodeError:
        return False
    except ObjectDoesNotExist:
        return False

