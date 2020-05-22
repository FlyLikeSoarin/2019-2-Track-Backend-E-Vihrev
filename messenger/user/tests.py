from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
import factory
import json


class TestUserViews(TestCase):
    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = 'user.User'

        username = factory.Sequence(lambda n: f'user{n}')
        email = factory.Sequence(lambda n: f'user{n}@mail.ru')
        password = factory.Sequence(lambda n: make_password(str(n)))

    def setUp(self):
        self.client = Client()
        for _ in range(10):
            self.UserFactory.create()
        token_response = self.client.post('/api/acquire-auth-token/', {'username': 'user1', 'password': '1'})
        self.token = token_response.data['token']

    def test_user_retrieve(self):
        response = self.client.get('/api/user/1/', Authorization=f'Token {self.token}')
        self.assertEqual('user1', response.data['username'])

    def test_user_list(self):
        response = self.client.get('/api/user/', Authorization=f'Token {self.token}')
        self.assertEqual(10, len(response.data))
