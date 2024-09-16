from django.contrib import admin
from book.models import Book, BookImage


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'publication_date', 'is_in_stock')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_date')


admin.site.register(BookImage)
