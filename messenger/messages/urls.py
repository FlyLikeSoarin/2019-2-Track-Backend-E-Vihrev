from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('get/', views.get_chat_messages, name='get-chat-messages'),
    path('send/', views.send_message, name='send-message')
]
