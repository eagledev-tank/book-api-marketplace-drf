from django.contrib import admin
from book.models import Book, BookImage


class BookImageInline(admin.StackedInline):
    model = BookImage
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_date')
    inlines = [BookImageInline]


admin.site.register(Book, BookAdmin)
admin.site.register(BookImage)
