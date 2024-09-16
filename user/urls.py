from rest_framework.routers import SimpleRouter
from .views import UserModelViewSet, ProfileModelViewSet
from django.urls import path, include


router = SimpleRouter()

router.register('User', UserModelViewSet, basename='user')
router.register('Profile', ProfileModelViewSet, basename='profile')

urlpatterns = [
]
