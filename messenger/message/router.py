from rest_framework.routers import DefaultRouter
from message.views import MessageViewSet

router = DefaultRouter()
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = router.urls
