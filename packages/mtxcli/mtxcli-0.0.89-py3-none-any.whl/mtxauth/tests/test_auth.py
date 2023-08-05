import json
import unittest
import boto3
from django.test import Client, TestCase, override_settings
from django.conf import settings
from django.urls import reverse
from mtlibs import jwt_helper
from django.contrib.auth import get_user_model
User = get_user_model()


class 登录_客户端(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.common_user = User.objects.create_user(username='staff@brown.edu', password='pw')
        self.admin = User.objects.create_user(
            username="admin@admin.com",
            email="admin@admin.com",
            password='pw',            
            is_superuser=True,
            is_staff=True
            )
        return super().setUp()

    def test_登录_GET(self):
        response = self.c.get(reverse('signin'))
        self.assertEqual(response.status_code, 405)
        # self.assertEqual(response.content, b'', "登录失败不返回任何提示")

    def test_登录_普通(self):
        response = self.c.post(reverse('signin'), 
                               data={
                                "username": self.admin.get_username(), 
                                "password": "pw"
                               },
                               
                               content_type='application/json')
        
        
        
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        jwt = response['token']
        self.assertGreater(len(response['token']),0)
        
        decodeJwt = jwt_helper.decode(jwt,settings.SECRET_KEY)
        self.assertIsNotNone(decodeJwt)
        self.assertEqual(decodeJwt["username"],self.admin.get_username())
        
        
    def test__登录_错误的私钥不能验证token(self):
        response = self.c.post(reverse('signin'), 
                               data={
                                "username": self.admin.get_username(), 
                                "password": "pw"
                               },                               
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        jwt = response['token']
        self.assertGreater(len(jwt),0)
        
        with self.assertRaises(Exception):
            jwt_helper.decode(jwt,settings.SECRET_KEY + "------")
            
            
    def test_注册_正常注册用户(self):        
        username = "new_user123"
        response = self.c.post(reverse('signup'), 
                               data={
                                "username": username, 
                                "password": "pw",
                                "email": "fake@email.com"
                               },                               
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        jwt = response['token']
         
        self.assertGreater(len(jwt),0)
        decodeJwt = jwt_helper.decode(jwt,settings.SECRET_KEY)
        self.assertIsNotNone(decodeJwt)
        self.assertEqual(decodeJwt["username"],username)
        
        
    def test_注册_用户已经存在(self):
        username = self.common_user.get_username()
        response = self.c.post(reverse('signup'), 
                               data={
                                "username": username, 
                                "password": "pw",
                                "email": "fake@email.com"
                               },                               
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['success'])
        
        
        
        
