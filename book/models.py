from django.db import models
from user.models import Profile


class Book(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookImage(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.image.name


class BookReview(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE) # отзыв qaysi kitobga tegishli
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['profile', 'book']

    def __str__(self):
        return f"{self.book.title} - {self.profile.user.email} ({self.rating} stars)"
