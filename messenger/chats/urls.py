from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('get/', views.get_chat_data, name='get-chat-data')
]
