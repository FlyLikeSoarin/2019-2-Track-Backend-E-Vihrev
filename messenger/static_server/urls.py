from django.contrib import admin
from django.urls import include, path
from static_server import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('lp-login/', views.lp_login, name='lp-login'),
]
