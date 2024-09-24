from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book, BookImage, BookReview
from .serializers import BookSerializer, BookImageSerializer, BookDetailSerializer, BookReviewSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .permission import IsOwner


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        # Update and delete allows to creator 
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        # For other actions all user can use it.
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['retrieve',]:
            return BookDetailSerializer
        return BookSerializer


class BookImageModelViewSet(ModelViewSet):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
    parser_classes = [MultiPartParser, FormParser]


class BookReviewModelViewSet(ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
