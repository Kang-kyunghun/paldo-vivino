import json
import bcrypt
import jwt

from django.test       import TestCase, Client
from unittest.mock     import patch, MagicMock

from paldo.settings    import SECRET_KEY, ALGORITHM
from .models           import Account, WishList
from product.models    import (Country,
                               Region,
                               Winery,
                               WineType,
                               Distributor,
                               Style,
                               Grape,
                               Product,
                               Vintage,
                               ProductGrape,
                               Rating)


def create_data():
    Account.objects.create(
        id          = 1,
        email       = 'admin@wecode.com',
        first_name  = 'Wecode',
        last_name   = "Wework",
        password    = '12345678'
    )

    Account.objects.create(
        id          = 2,
        email       = 'kgh239@wecode.com',
        first_name  = 'Wecode',
        last_name   = "Wework",
        password    = '12345678'
    )

    Country.objects.create(
            id = 1,
            name = 'Korea'
        )

    Region.objects.create(
        id = 1,
        name = 'JeJu'
    )
   
    WineType.objects.create(
        id = 1,
        name = 'Soju'
    )
  
    Style.objects.create(
        id = 1,
        name = 'Korean Soju'
    )
    
    Winery.objects.create(
        id = 1,
        name = 'Lotte'
    )
    
    Distributor.objects.create(
        id = 1,
        name = 'Doosan'
    )
    
    Grape.objects.create(
        id = 1,
        name = '-'
    )
    
    Product.objects.create(
        id              = 1,
        name            = 'HanRaSan',
        image           = 'HanRaSan.png',
        country         = Country.objects.get(id=1),
        region          = Region.objects.get(id=1),
        wine_type       = WineType.objects.get(id=1),
        winery          = Winery.objects.get(id=1),
        style           = Style.objects.get(id=1),
        distributor     = Distributor.objects.get(id=1),
        alcohol_content = 16.7,
        allergen        = 'Contains sulfites',
        highlight       = 'Highlight1.\u2028Highlight2.',
        taste_summary   = 'The taste profile of HanRaSan  is based on 7760 user reviews',
        bold            = 0,
        sweet           = 10,
        acidic          = 0,
    )
    
    Vintage.objects.create(
        id             = 1,
        product        = Product.objects.get(id = 1),
        year           = 2019,
        price          = 23.8,
        feature        = 'feature1',
        stock          = 13,   
    )
    
    ProductGrape.objects.create(
        product  = Product.objects.get(id=1),
        grape    = Grape.objects.get(id=1)
    )
    WishList.objects.create(
        user    = Account.objects.get(id = 2),
        vintage = Vintage.objects.get(id = 1)
    )

def delete_data():
    Country.objects.all().delete()
    Region.objects.all().delete()
    WineType.objects.all().delete()
    Winery.objects.all().delete()
    Style.objects.all().delete()
    Grape.objects.all().delete()
    Distributor.objects.all().delete()
    Product.objects.all().delete()
    Vintage.objects.all().delete()
    ProductGrape.objects.all().delete()
    Rating.objects.all().delete()
    Account.objects.all().delete()
    WishList.objects.all().delete()

class SignUpTest(TestCase):

    def setUp(self):
        Account.objects.create(
            email      = 'wecode@naver.com',
            first_name = 'Wecode',
            last_name  = 'Wework',
            password   =  '123456789'
        )
        
    def tearDown(self):
        Account.objects.all().delete()

    def test_signupview_post_success(self):
        client = Client()
        user = {
            'email'      : 'kgh239@naver.com',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_signupview_post_fail_duplication(self):
        client = Client()
        user = {
            'email'      : 'wecode@naver.com',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_EMAIL'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_emailformat1(self):
        client = Client()
        user = {
            'email'      : 'wecodenaver.com',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'NOT INCLUDE @ or . '
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_emailformat2(self):
        client = Client()
        user = {
            'email'      : 'wecode@navercom',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'NOT INCLUDE @ or . '
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_passwordlenght(self):
        client = Client()
        user = {
            'email'      : 'kgh239@naver.com',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '12345' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'PASSWORD TOO SHORT'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_keyerror(self):
        client = Client()
        user = {
            'emaisl'     : 'kgh239@naver.com',
            'first_name' : 'Kyunghun',
            'last_name'  : 'Kang',
            'password'   :  '12345' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )
        self.assertEqual(response.status_code, 400)

class WishListTest(TestCase):
    def setUp(self):
        create_data()

    def tearDown(self):
        delete_data()

    def test_wishlist_add_success(self):
        client = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token}
        
        response = client.patch("/accounts/wishlist/1", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message' : 'WISHLIST_ADD'
            }
        )
    
    def test_wishlist_delete_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token}
        
        response = client.patch("/accounts/wishlist/1", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message' : 'WISHLIST_DELETE'
            }
        )
    
    def test_wishlist_get_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token}
        
        response = client.get("/accounts/wishlist", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "products": {
                        "profile" :{
                                    "profile_image" : None
                                   },
                        "count"  : 1,
                        "result" : [
                                    {
                                        "id": 1,
                                        "image_url": "HanRaSan.png",
                                        "winery": "Lotte",
                                        "wine_name": "HanRaSan",
                                        "year": 2019,
                                        "nation": "Korea",
                                        "region": "JeJu",
                                        "rating": 0.0,
                                        "ratings": 0,
                                        "price": "23.80",
                                        "percentage" : None,
                                        "feature": "feature1",
                                        "editor_note": None
                                    }]
            }       
        })