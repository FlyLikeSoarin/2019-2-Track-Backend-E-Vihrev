from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('user.router')),
    path('', include('chat.router')),
    path('', include('message.router')),
    path('acquire-auth-token/', views.obtain_auth_token),
]
