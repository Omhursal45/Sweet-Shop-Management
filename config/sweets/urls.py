# sweets/urls.py
from rest_framework.routers import DefaultRouter
from .views import SweetViewSet

router = DefaultRouter()
router.register(r'', SweetViewSet, basename='sweet')  

urlpatterns = router.urls
