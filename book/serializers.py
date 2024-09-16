from rest_framework.serializers import ModelSerializer
from .models import Book, BookImage
from user.serializers import ProfileSerializer
from rest_framework import serializers
from .validators import description_validator


class BookImageSerializer(ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'


class BookSerializer(ModelSerializer):
    description = serializers.CharField(validators=[description_validator])
    profile_obj = ProfileSerializer(source='profile', read_only=True)
    image_obj = BookImageSerializer(source='bookimage_set', many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].upper()
        return super().create(validated_data)
