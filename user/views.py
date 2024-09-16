from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.viewsets import ModelViewSet


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileModelViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
