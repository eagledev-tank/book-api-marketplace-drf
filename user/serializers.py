from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
