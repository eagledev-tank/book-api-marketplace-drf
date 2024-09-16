from rest_framework.routers import SimpleRouter
from .views import BookModelViewSet, BookImageModelViewSet
from django.urls import path, include


router = SimpleRouter()

router.register('Book', BookModelViewSet, basename='book')
router.register('BookImage', BookImageModelViewSet, basename='book-image')

urlpatterns = [
]
