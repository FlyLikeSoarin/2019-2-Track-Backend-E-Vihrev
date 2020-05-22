from django.test import TestCase, Client
from unittest.mock import patch
from django.contrib.auth.hashers import make_password

import factory
import json

from user.models import User


class TestChatViews(TestCase):
    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = 'user.User'

        username = factory.Sequence(lambda n: f'user{n}')
        email = factory.Sequence(lambda n: f'user{n}@mail.ru')
        password = factory.Sequence(lambda n: make_password(str(n)))

    class ChatFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = 'chat.Chat'

        creator = factory.Sequence(lambda n: User.get_by_username(f'user{n}'))
        chat_label = factory.Sequence(lambda n: f'chat_of_user{n}')

    def setUp(self):
        self.client = Client()
        for _ in range(10):
            self.UserFactory.create()
            self.ChatFactory.create()
        token_response = self.client.post('/api/acquire-auth-token/', {'username': 'user1', 'password': '1'})
        self.token = token_response.data['token']

    @patch('chat.views.ChatViewSet')
    def test_send_message(self, ChatViewSet_mock):
        response = self.client.get('/api/chat/1/list_messages/', Authorization=f'Token {self.token}')
        self.assertEqual(0, len(response.data['messages']))

        response = self.client.post('/api/user/1/send_message/', {'text': 'Hi!'}, Authorization=f'Token {self.token}')

        response = self.client.get('/api/chat/1/list_messages/', Authorization=f'Token {self.token}')
        self.assertEqual(0, len(response.data['messages']))
        self.assertEqual('Hi!', response.data['Hi!'])
        self.assertTrue(ChatViewSet_mock.called)

    def test_chat_list(self):
        response = self.client.get('/api/chat/', Authorization=f'Token {self.token}')
        self.assertEqual(10, len(response.data))
