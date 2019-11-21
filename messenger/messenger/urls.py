from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('messages/', include('message.urls')),
    path('', include('static_server.urls'))
]
