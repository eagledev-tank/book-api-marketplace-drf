from rest_framework.serializers import ModelSerializer
from .models import Book, BookImage, BookReview
from user.serializers import ProfileSerializer
from rest_framework import serializers
from .validators import description_validator
from django.db.models import Avg


class BookImageSerializer(ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'


class BookSerializer(ModelSerializer):
    image_obj = BookImageSerializer(source='bookimage_set', many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = 'profile',

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].upper()

        user = self.context['request'].user
        profile = user.profile
        book = Book.objects.create(profile=profile, **validated_data)

        return book

    def update(self, instance, validated_data):
        validated_data['title'] = validated_data.get('title', None).capitalize()
        return super().update(instance, validated_data)


class BookReviewSerializer(ModelSerializer):
    """
    Serializer for review model
    """
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = BookReview
        fields = ['profile', 'book', 'rating', 'comment', 'created_at']


class BookDetailSerializer(ModelSerializer):
    description = serializers.CharField(validators=[description_validator])
    profile_obj = ProfileSerializer(source='profile', read_only=True)
    image_obj = BookImageSerializer(source='bookimage_set', many=True, read_only=True)
    title = serializers.SerializerMethodField()
    review_objs = BookReviewSerializer(source='reviews', many=True, read_only=True)
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_title(self, obj):
        return obj.title.upper()

    def get_total_reviews(self, obj):
        reviews = BookReview.objects.filter(book=obj)
        context = {
            'reviews_count': reviews.count(),
            'reviews_avg_rating': reviews.aggregate(Avg('rating'))['rating__avg']
        }
        return context
