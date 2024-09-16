from django.db import models
from user.models import Profile


class Book(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_in_stock(self):
        return self.stock > 0

    # def save(self, *args, **kwargs):
    #     self.title = self.title.upper()
    #     super(Book, self).save(*args, **kwargs)


class BookImage(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.image.name
