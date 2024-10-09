from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


#########################################################################################
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import authenticate


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Email tasdiqlash uchun email yuboramiz
        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://127.0.0.1:8000/api/v1/user/activation/{uidb64}/{token}/"
        send_mail(
            'Email Tasdiqlash',
            f"Email tasdiqlash uchun quyidagi havolaga bosing: {activation_link}",
            'nurislomlapasov@gmail.com',
            [user.email],
        )


class ActivateAccountSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Noto\'g\'ri havola')

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError('Havola amal qilish muddati tugagan')

        user.is_active = True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Noto\'g\'ri email yoki parol")

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            raise serializers.ValidationError("Refresh token majburiy")

        return data


class ProfileSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def send_reset_email(self, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/api/v1/user/password_reset_confirm/{uidb64}/{token}/"
        send_mail(
            'Parolni tiklash',
            f"Parolni tiklash uchun quyidagi havolaga bosing: {reset_link}",
            'nurislomlapasov@gmail.com',
            [user.email],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar bir xil bo'lishi kerak")
        elif len(data['confirm_password']) < 8:
            raise serializers.ValidationError("Password 8 ta belgidan kam bo'lmasligi kerak")
        return data
