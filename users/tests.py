import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acount_book.settings")
import django
django.setup()

from django.test import TestCase, Client
from users.models import MyUser

# Create your tests here.

class TestUser(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user(
            username="woshixiaohei",
            password="nishihaoren"
        )
        user.save()
        self.client = Client()


    def test_create_user(self):
        user = MyUser.objects.create_superuser(
            username="testuser",
            password="testuser",
            email="2q3dapkd@qq.com"
        )
        self.assertEqual(user.is_superuser, True)
        user = MyUser.objects.create_user_auto()
        self.assertIsNotNone(user.username)
        user = MyUser.objects.create_user_with_openid("testopenid")
        self.assertIsNotNone(user.username)

    def test_register(self):
        data = {
            "username": "testuser",
            "password": "testuser"
        }
        response = self.client.post(
            '/users/register/',
            data=data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json_data['token'])

    def test_logout_failure(self):
        response = self.client.post(
            '/users/logout/',
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data['detail'], 'Authentication credentials were not provided.')

    def test_logout_success(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        response = self.client.post(
            '/users/logout/',
            headers=headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

    def test_user_profile(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        response = self.client.get(
            '/users/profile/',
            headers=headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['username'], "woshixiaohei")

    def test_user_profile_patch(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            "nickname": "xiaobai"
        }
        response = self.client.patch(
            '/users/profile/',
            data=data,
            headers=headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['nickname'], "xiaobai")
    
    def test_user_profile_put(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            "nickname": "xiaobai",
        }
        response = self.client.put(
            '/users/profile/',
            data=data,
            headers=headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['nickname'], "xiaobai")

    def test_user_profile_post(self):
        data = {
            "username": "woshixiaohei",
            "password": "nishihaoren",
        }
        response = self.client.post(
            '/users/login/',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            "avatar": "http://www.baidu.com",
        }
        response = self.client.post(
            '/users/profile/',
            data=data,
            headers=headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_wxlogin(self):
        data = {
            "code": "testcode"
        }
        response = self.client.post(
            '/users/wxlogin/',
            data=data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()