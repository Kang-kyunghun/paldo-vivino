import json
import bcrypt

from django.test       import TestCase, Client
from unittest.mock     import patch, MagicMock
from .models           import Account

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
            'email' : 'kgh239@naver.com',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_signupview_post_fail_duplication(self):
        client = Client()
        user = {
            'email' : 'wecode@naver.com',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'DUPLICATED_EMAIL'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_emailformat1(self):
        client = Client()
        user = {
            'email' : 'wecodenaver.com',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'NOT INCLUDE @ or . '
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_emailformat2(self):
        client = Client()
        user = {
            'email' : 'wecode@navercom',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '123456789' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'NOT INCLUDE @ or . '
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_passwordlenght(self):
        client = Client()
        user = {
            'email' : 'kgh239@naver.com',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '12345' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'PASSWORD TOO SHORT'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signupview_post_fail_keyerror(self):
        client = Client()
        user = {
            'emaisl' : 'kgh239@naver.com',
            'first_name': 'Kyunghun',
            'last_name': 'Kang',
            'password' :  '12345' }
        response = client.post('/accounts/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )
        self.assertEqual(response.status_code, 400)