import json
import bcrypt
import jwt

from django.test       import TestCase, Client
from unittest.mock     import patch, MagicMock

from paldo.settings    import SECRET_KEY, ALGORITHM
from .models           import Cart 
from account.models    import Account, WishList
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
    Cart.objects.create(
        id      = 1,
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
    Cart.objects.all().delete()

class CartsTest(TestCase):
    def setUp(self):
        create_data()

    def tearDown(self):
        delete_data()

    def test_carts_get_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
        
        response  = client.get("/orders/carts", **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "cart_list": {
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
                                        "quantity" : 1
                                    }]
                        }
                
            }
        )

    def test_carts_post_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
        data = {
            "vintage_id" : "1",  
            "quantity"   : "1"
        }
       
        response = client.post("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'ADD_SUCCESS'
            }
        )

    def test_carts_change_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
        data = {
            "vintage_id" : "1",  
            "quantity"   : "3"
        }
       
        response = client.post("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'CHANGE_SUCCESS'
            }
        )

    def test_carts_post_keyerror_fail(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token,
                  'content_type'       : 'application/json'
        }
        data = {
            "id"         : "1",  
            "quantity"   : "3"
        }
       
        response = client.post("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )
    
    def test_carts_delete_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 2)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
       
        response = client.delete("/orders/carts/1", **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )
        
    def test_carts_delete_invaliduser_fail(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
       
        response = client.delete("/orders/carts/1", **headers)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_USER'
            }
        )
    
    def test_carts_delete_donotexist_fail(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers = {'HTTP_Authorization' : access_token,
                  'content_type'        : 'application/json'
        }
       
        response  = client.delete("/orders/carts/100", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'CART_DOES_NOT_EXIST'
            }
        )

    def test_carts_update_success(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token,
                  'content_type'       : 'application/json'
        }
        data = {
            "id"       : "1",  
            "quantity" : "2"
        }
       
        response  = client.patch("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'patch':{
                    "cart_id"        : 1,
                    "befor_quantity" : 1,
                    "after_quantity" : 2
                }
            }
        )
    
    def test_carts_invalid_id_fail(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token,
                  'content_type'       : 'application/json'
        }
        data = {
            "id"       : "100",  
            "quantity" : "2"
        }
       
        response  = client.patch("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'CART_DOES_NOT_EXIST'
            }
        )
    
    def test_carts_patch_keyerror_fail(self):
        client       = Client()
        access_user  = Account.objects.get(id = 1)
        access_token = jwt.encode({'user_id': access_user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        headers= {'HTTP_Authorization' : access_token,
                  'content_type'       : 'application/json'
        }
        data = {
            "idd"      : "100",  
            "quantity" : "2"
        }
       
        response  = client.patch("/orders/carts", json.dumps(data), **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )