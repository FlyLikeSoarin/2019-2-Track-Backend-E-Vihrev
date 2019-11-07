from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('chat/', include('chats.urls')),
    path('messages/', include('messages.urls')),
    path('', include('static_server.urls'))
]
