import json
import bcrypt
import jwt
import boto3
import requests
import re

from random             import randint
from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from paldo.settings     import SECRET_KEY, ALGORITHM, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from utils              import login_decorator
from .models            import Account, WishList
from product.models     import Vintage

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            PASSWORD_LENGTH = 8
            
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'DUPLICATED_EMAIL'}, status=400)
            
            if re.findall('[@.]', data['email']) != ['@', '.']:
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

class WishListView(View):
    @login_decorator
    def patch(self, request, id):
        if not WishList.objects.filter(user_id = request.user_id, vintage_id = id).exists():
            WishList.objects.create(
                user_id    = request.user_id,
                vintage_id = id
            )
            return JsonResponse({'message':'WISHLIST_ADD'}, status=200)
        
        WishList.objects.get(user_id = request.user_id, vintage_id = id).delete()
        return JsonResponse({'message':'WISHLIST_DELETE'}, status=200)

    @login_decorator
    def get(self, request):
        wishlists = WishList.objects.select_related('vintage__product__winery', 
                                                    'vintage__product__country', 
                                                    'vintage__product__region')\
                                                    .filter(user_id = request.user_id)
        products = {
            "profile" :{
                            "profile_image" : Account.objects.get(id = request.user_id).image
                       },
            "count"   : wishlists.count(),
            "result"  : [{
                            "id"          : wishlist.vintage.id,
                            "image_url"   : wishlist.vintage.product.image,
                            "winery"      : wishlist.vintage.product.winery.name,
                            "wine_name"   : wishlist.vintage.product.name,
                            "year"        : wishlist.vintage.year,
                            "nation"      : wishlist.vintage.product.country.name,
                            "region"      : wishlist.vintage.product.region.name,
                            "rating"      : wishlist.vintage.average_score,
                            "ratings"     : wishlist.vintage.total_rating,
                            "price"       : wishlist.vintage.price,
                            "percentage"  : wishlist.vintage.discount_rate,
                            "feature"     : wishlist.vintage.feature,
                            "editor_note" : wishlist.vintage.edit_note
                        } for wishlist in wishlists]
        }

        return JsonResponse({'products':products}, status=200)

class ProfileImageView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    @login_decorator
    def post(self, request):
        file = request.FILES['filename']

        url = str(request.user_id)   
        self.s3_client.upload_fileobj(
            file, 
            "kyunghun-s3",
            url,
            ExtraArgs={
                "ContentType": file.content_type
            }
        ) 
        URL = f'https://kyunghun-s3.s3.ap-northeast-2.amazonaws.com/{url}'
        if Account.objects.get(id = request.user_id) == None:
            Account.objects.update(image = URL)
        else:
            Account.objects.filter(id = request.user_id).update(image = URL)
        return JsonResponse({'message':'SUCCESS'}, status=200)
            
class SignInView(View):
    def post(self, request):           
        data = json.loads(request.body)
        try:
            if not Account.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=403)

            if not bcrypt.checkpw(
                data['password'].encode('utf-8'), Account.objects.get(email=data['email']).password.encode('utf-8')):                
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            accessed_user = Account.objects.get(email=data['email'])
            access_token  = jwt.encode({'user_id': accessed_user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'Authorization': access_token.decode('utf-8')}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request):           
       
        token          = request.headers.get('AccessToken')
        URL            = 'https://kapi.kakao.com/v2/user/me'
        headers        = {'Authorization': f'Bearer {token}'}
        response_kakao = requests.post(URL, headers = headers)
        data           = response_kakao.json()
        data_kakao     = data['kakao_account']

        try:
            if not Account.objects.filter(email=data_kakao['email']).exists():
                encoded_password = str(randint(1000000000000,9999999999999)).encode('utf-8')
                hashed_pw        = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                Account.objects.create(
                    email      = data_kakao['email'],
                    first_name = '-',
                    last_name  = data_kakao['profile']['nickname'],
                    password   = hashed_pw.decode('utf-8') 
                )
            accessed_user = Account.objects.get(email=data_kakao['email'])
            access_token  = jwt.encode({'user_id': accessed_user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'Authorization': access_token.decode('utf-8')}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
