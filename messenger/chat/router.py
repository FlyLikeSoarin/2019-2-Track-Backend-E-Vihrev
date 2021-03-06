from rest_framework.routers import DefaultRouter
from chat.views import ChatViewSet

router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename='chat')

urlpatterns = router.urls
