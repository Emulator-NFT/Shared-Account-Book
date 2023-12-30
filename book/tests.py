import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acount_book.settings")
import django
django.setup()

from django.test import TestCase, Client
from users.models import MyUser

class TestLedger(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user(
            username="woshixiaohei",
            password="nishihaoren"
        )
        user.save()
        self.client = Client()
        self.headers = self.login()

    def login(self):
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
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        return headers

    def test_ledger_create(self):
        data = {
            "title": "test_ledger",
            "description": "test_ledger",
            "ledger_type": "personal"
        }
        response = self.client.post(
            '/book/ledgers/',
            headers=self.headers,
            data=data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertIsNotNone(json_data['id'])
        id = json_data['id']
        # retrieve
        response = self.client.get(
            f'/book/ledgers/{id}/',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
    
    def test_ledger_list(self):
        response = self.client.get(
            '/book/ledgers/?ledger_type=personal',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
    
    def test_logout_success(self):
        response = self.client.post(
            '/users/logout/',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

class TestEntry(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user(
            username="woshixiaohei",
            password="nishihaoren"
        )
        user.save()
        self.client = Client()
        self.headers = self.login()
        self.ledger_id = self.create_ledger()
        self.categories = self.get_category()
        self.entries = self.create_entries()
    
    def login(self):
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
        self.token = json_data['token']
        headers = {
            'Authorization': 'Token ' + self.token
        }
        return headers
    
    def create_ledger(self):
        data = {
            "title": "test_ledger",
            "description": "test_ledger",
            "ledger_type": "group"
        }
        response = self.client.post(
            '/book/ledgers/',
            headers=self.headers,
            data=data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertIsNotNone(json_data['id'])
        id = json_data['id']
        return id
    
    def get_category(self):
        response = self.client.get(
            f'/book/categories/?ledger={self.ledger_id}&category_type=expense',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f'/book/categories/?ledger={self.ledger_id}',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 22)
        categories = []
        for data in json_data:
            categories.append(data['id'])
        return categories
    
    def test_create_entry(self):
        data = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "4个包子",
            "amount": -16.9,
            "entry_type": "expense",
            "category": self.categories[6]
        }
        response = self.client.post(
            '/book/entries/',
            headers=self.headers,
            data=data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertIsNotNone(json_data['id'])
        id = json_data['id']
        # retrieve
        response = self.client.get(
            f'/book/entries/{id}/',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def create_entries(self):
        data1 = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "4个包子",
            "amount": -16.9,
            "entry_type": "expense",
            "category": self.categories[6]
        }
        data2 = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "牛肉面",
            "amount": -30.0,
            "entry_type": "expense",
            "category": self.categories[7]
        }
        data3 = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "鸡肉",
            "amount": -200.0,
            "entry_type": "expense",
            "category": self.categories[8]
        }

        data4 = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "yu肉",
            "amount": -300.0,
            "entry_type": "expense",
            "category": self.categories[9]
        }

        data5 = {
            "ledgers": [
                self.ledger_id
            ],
            "title": "工资",
            "amount": 10000.0,
            "entry_type": "income",
            "category": self.categories[0]
        }

        data = [data1, data2, data3, data4, data5]
        entries = []
        for d in data:
            response = self.client.post(
                '/book/entries/',
                headers=self.headers,
                data=d,
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 201)
            json_data = response.json()
            self.assertIsNotNone(json_data['id'])
            entries.append(json_data['id'])
        return entries

    def test_entry_list(self):
        response = self.client.get(
            f'/book/entries/?ledger={self.ledger_id}&?entry_type=expense&?category={self.categories[6]}&?date_from=2023-12-20&?date_to=2023-12-31&amount_from=0&amount_to=10000',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
       
        response = self.client.get(
            f'/book/entries/?ledger={self.ledger_id}&?review_status=unreviewed?&?search=yu',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f'/book/entries/?ledger={self.ledger_id}&?ordering=id',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f'/book/entries/?ledger={self.ledger_id}&?ordering=amount',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_entry_review(self):
        entry_id = self.entries[0]
        response = self.client.patch(
            f'/book/entries/{entry_id}/review/',
            headers=self.headers,
            data={"review_status": "approved"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

    def test_entry_subreview(self):
        entry_id = self.entries[0]
        response = self.client.patch(
            f'/book/entries/{entry_id}/subreview/',
            headers=self.headers,
            data={"review_status": "unreviewed"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

    def test_ledger_analysis(self):
        response = self.client.get(
            f'/book/ledgers/{self.ledger_id}/analysis/?year=2023&month=12',
            headers=self.headers,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()