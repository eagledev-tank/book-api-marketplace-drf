from .models import Book, BookImage
from .serializers import BookSerializer, BookImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookImageModelViewSet(ModelViewSet):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
    parser_classes = [MultiPartParser, FormParser]
