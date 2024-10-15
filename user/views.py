# from .models import User, Profile
# from .serializers import UserSerializer, ProfileSerializer
# from rest_framework.viewsets import ModelViewSet
#
#
# class UserModelViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class ProfileModelViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

###########################################################################################

from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Profile, User
from .serializers import (
    RegisterSerializer, ActivateAccountSerializer,
    LoginSerializer, ProfileSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    LogoutSerializer, ProfileUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ActivateAccountView(generics.GenericAPIView):
    serializer_class = ActivateAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response({'message': 'Akkount muvaffaqiyatli faollashtirildi'}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = serializer.get_token(user)
        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh_token']
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()

            return Response({"message": "Tizimdan chiqdingiz, refresh token bekor qilindi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'])
        serializer.send_reset_email(user)
        return Response({"message": "Email yuborildi"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Havola amal qilish muddati tugagan"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Parol yangilandi"}, status=status.HTTP_200_OK)


class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile
