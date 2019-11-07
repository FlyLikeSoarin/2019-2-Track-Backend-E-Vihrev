from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('me/', views.get_my_profile, name='get-my-profile'),
    path('profile/', views.get_user_profile, name='get-user-profile'),
    path('friends/', views.get_user_friends, name='get-user-friends'),
    path('chats/', views.get_user_chats, name='get-user-chats'),
    path('register/', views.register_user, name='register-user')
]
