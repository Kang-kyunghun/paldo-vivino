import json

from django.test     import TestCase
from django.test     import Client
from unittest.mock   import patch, MagicMock

from account.models  import Account
from .models         import (Country,
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
    Country.objects.create(
            id = 1,
            name = 'Korea'
        )
    Country.objects.create(
        id = 2,
        name = 'France'
    )
    Region.objects.create(
        id = 1,
        name = 'JeJu'
    )
    Region.objects.create(
        id = 2,
        name = 'Paris'
    )
    WineType.objects.create(
        id = 1,
        name = 'Soju'
    )
    WineType.objects.create(
        id = 2,
        name = 'Red'
    )
    Style.objects.create(
        id = 1,
        name = 'Korean Soju'
    )
    Style.objects.create(
        id = 2,
        name = 'France wine'
    )
    Winery.objects.create(
        id = 1,
        name = 'Lotte'
    )
    Winery.objects.create(
        id = 2,
        name = 'Wecode'
    )
    Distributor.objects.create(
        id = 1,
        name = 'Doosan'
    )
    Distributor.objects.create(
        id = 2,
        name = 'Vivino'
    )
    Grape.objects.create(
        id = 1,
        name = '-'
    )
    Grape.objects.create(
        id = 2,
        name = 'Grape'
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
    Product.objects.create(
        id              = 2,
        name            = 'France red wine',
        image           = 'France_red_wine.png',
        country         = Country.objects.get(id=2),
        region          = Region.objects.get(id=2),
        wine_type       = WineType.objects.get(id=2),
        winery          = Winery.objects.get(id=2),
        style           = Style.objects.get(id=2),
        distributor     = Distributor.objects.get(id=2),
        alcohol_content = 12.7,
        allergen        = 'Contains sulfites',
        highlight       = 'Highlight1.\u2028Highlight2.',
        taste_summary   = 'taste_summary_red',
        bold            = 20,
        sweet           = 10,
        acidic          = 20,
    )
    Vintage.objects.create(
        id             = 1,
        product        = Product.objects.get(id = 1),
        year           = 2019,
        price          = 23.8,
        feature        = 'feature1',
        stock          = 13,   
    )
    Vintage.objects.create(
        id             = 2,
        product        = Product.objects.get(id = 1),
        year           = 2018,
        price          = 22.1,
        feature        = 'feature2',
        stock          = 5,
        average_score  = 4.5   
    )
    Vintage.objects.create(
        id             = 3,
        product        = Product.objects.get(id = 2),
        year           = 2011,
        price          = 43.1,
        feature        = 'feature3',
        stock          = 1,
        average_score  = 4.3
    )
    Vintage.objects.create(
        id             = 4,
        product        = Product.objects.get(id = 2),
        year           = 2010,
        price          = 41.1,
        feature        = 'feature4',
        stock          = 2,
        average_score  = 4.0
    )
    Vintage.objects.create(
        id             = 5,
        product        = Product.objects.get(id = 2),
        year           = 2009,
        price          = 42.1,
        feature        = "feature5",
        stock          = 3,
        average_score  = 4.2,
        total_rating   = 256,
        edit_note      = "Editor_note1",
        description    = "description1",
        vin            = "vin1",
        domaine        = "domaine1",
        vignoble       = "vignoble1",
    )
    ProductGrape.objects.create(
        product  = Product.objects.get(id=1),
        grape    = Grape.objects.get(id=1)
    )
    ProductGrape.objects.create(
        product  = Product.objects.get(id=2),
        grape    = Grape.objects.get(id=2)
    )
    for i in range(1,6):
        Rating.objects.create(
            user    = Account.objects.get(id=1),
            vintage = Vintage.objects.get(id=5),
            grade   = i
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

class ProductsTest(TestCase):

    def setUp(self):
        create_data()
        
    def tearDown(self):
        delete_data()
        
    def test_procuts_get_success(self):
        client = Client()
        response = client.get('/products')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count"  : 5,
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
                                    },
                                    {
                                        "id": 2,
                                        "image_url": "HanRaSan.png",
                                        "winery": "Lotte",
                                        "wine_name": "HanRaSan",
                                        "year": 2018,
                                        "nation": "Korea",
                                        "region": "JeJu",
                                        "rating": 4.5,
                                        "ratings": 0,
                                        "price"  : "22.10",
                                        "percentage": None,
                                        "feature": "feature2",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_procuts_get_filter_region_success(self):
        client = Client()
        response = client.get('/products?region=Paris')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 3,
                        "result": [
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)
    
    def test_procuts_get_filter_price_success(self):
        client = Client()
        response = client.get('/products?price_low=23&price_high=45')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 4,
                        "result": [
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
                                        "percentage": None,
                                        "feature": "feature1",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_procuts_get_filter_rating_success(self):
        client = Client()
        response = client.get('/products?rating=4')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 4,
                        "result": [
                                    {
                                        "id": 2,
                                        "image_url": "HanRaSan.png",
                                        "winery": "Lotte",
                                        "wine_name": "HanRaSan",
                                        "year": 2018,
                                        "nation": "Korea",
                                        "region": "JeJu",
                                        "rating": 4.5,
                                        "ratings": 0,
                                        "price"  : "22.10",
                                        "percentage": None,
                                        "feature": "feature2",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)
    
    def test_procuts_get_filter_type_success(self):
        client = Client()
        response = client.get('/products?type=Red')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 3,
                        "result": [
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_procuts_get_order_success(self):
        client = Client()
        response = client.get('/products?order=-average_score')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 5,
                        "result": [     
                                    {
                                        "id": 2,
                                        "image_url": "HanRaSan.png",
                                        "winery": "Lotte",
                                        "wine_name": "HanRaSan",
                                        "year": 2018,
                                        "nation": "Korea",
                                        "region": "JeJu",
                                        "rating": 4.5,
                                        "ratings": 0,
                                        "price"  : "22.10",
                                        "percentage": None,
                                        "feature": "feature2",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },
                                    {

                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
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
                                        "percentage": None,
                                        "feature": "feature1",
                                        "editor_note": None
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)
    
    def test_procuts_get_filter_style_success(self):
        client = Client()
        response = client.get('/products?style=France wine')
       
        self.assertEqual(response.json(),
            {
            "products": {
                        "count": 3,
                        "result": [{
                                        "id": 3,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2011,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.3,
                                        "ratings": 0,
                                        "price"  : "43.10",
                                        "percentage": None,
                                        "feature": "feature3",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 4,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2010,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.0,
                                        "ratings": 0,
                                        "price"  : "41.10",
                                        "percentage": None,
                                        "feature": "feature4",
                                        "editor_note": None
                                    },
                                    {
                                        "id": 5,
                                        "image_url": "France_red_wine.png",
                                        "winery": "Wecode",
                                        "wine_name": "France red wine",
                                        "year": 2009,
                                        "nation": "France",
                                        "region": "Paris",
                                        "rating": 4.2,
                                        "ratings": 256,
                                        "price"  : "42.10",
                                        "percentage": None,
                                        "feature": "feature5",
                                        "editor_note": "Editor_note1"
                                    },]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_procuts_get_filter_type_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?type=RRed')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_procuts_get_filter_region_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?region=JJeju')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)

    def test_procuts_get_filter_country_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?country=Corea')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)

    def test_procuts_get_filter_style_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?style=STYLE')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)

    def test_procuts_get_filter_rating_MINIMUM_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?rating=-1')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)

    def test_procuts_get_filter_rating_MAXIMUM_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?rating=6')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)

    def test_procuts_get_filter_price_MINIMUM_invalidvalue_fail(self):
        client = Client()
        response = client.get('/products?price_low=-1')
       
        self.assertEqual(response.json(),
            {
            'message': 'INVALID_VALUE'
        })
        self.assertEqual(response.status_code, 400)      

class ProductTest(TestCase):
    def setUp(self):
        create_data()
        
    def tearDown(self):
        delete_data()

    def test_procut_get_success(self):
        client = Client()
        response = client.get('/products/5')
       
        self.assertEqual(response.json(),
            {
            "product": {
                            "id": 5,
                            "image_url": "France_red_wine.png",
                            "type" : "Red",
                            "winery": "Wecode",
                            "wine_name": "France red wine",
                            "year": 2009,
                            "nation": "France",
                            "region": "Paris",
                            "rating": 4.2,
                            "ratings": 256,
                            "price": "42.10",
                            "percentage": None,
                            "feature": "feature5",
                            "editor_note": "Editor_note1",
                            "merchant": "Vivino",
                            "description": [
                                "description1",
                                "vin1",
                                "domaine1",
                                "vignoble1"
                            ],
                            "highlight": [
                                "Highlight1.",
                                "Highlight2."
                            ],
                            "taste_summary": "taste_summary_red",
                            "bold": "20.00",
                            "sweet": "10.00",
                            "acidic": "20.00",
                            "score": [
                                1,
                                1,
                                1,
                                1,
                                1
                            ],
                            "wishlist" : False,
                            "grape"           : ['Grape'],
                            "alcohol_content" : '12.70',
                            "allergen"        : 'Contains sulfites',
                            "vintages": [
                                {
                                    "id": 3,
                                    "year": 2011,
                                    "rating": 4.3,
                                    "ratings": 0,
                                    "price": "43.10",
                                    "percentage": None,
                                    "feature": "feature3"
                                },
                                {
                                    "id": 4,
                                    "year": 2010,
                                    "rating": 4.0,
                                    "ratings": 0,
                                    "price": "41.10",
                                    "percentage": None,
                                    "feature": "feature4"
                                },
                                {
                                    "id": 5,
                                    "year": 2009,
                                    "rating": 4.2,
                                    "ratings": 256,
                                    "price": "42.10",
                                    "percentage": None,
                                    "feature": "feature5"
                                },
                            ]
                        }
        })
        self.assertEqual(response.status_code, 200)
    
    def test_Product_get_fail(self):
        client = Client()
        response = client.get('/products/100')
        self.assertEqual(response.json(),
            {
                'message':'ObjectDoesNotExist'
            }
        )
        self.assertEqual(response.status_code, 400)