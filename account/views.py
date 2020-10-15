import json
import bcrypt
import jwt
import boto3

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

class WishListView(View):
    @login_decorator
    def patch(self, request, id):
        if not WishList.objects.filter(user_id = request.user_id, vintage_id = id).exists():
            WishList.objects.create(
                user_id    = request.user_id,
                vintage_id = id
            )
            return JsonResponse({'message':'WISHLIST_ADD'}, status=200)
        
        WishList.objects.filter(user_id = request.user_id, vintage_id = id).delete()
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