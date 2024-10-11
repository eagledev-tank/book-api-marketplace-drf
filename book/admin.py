from django.contrib import admin
from book.models import Book, BookImage
from order.models import OrderItem
from django.db.models import Sum, F


class BookImageInline(admin.StackedInline):
    model = BookImage
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'publication_date',
                    'is_in_stock', 'total_sold', 'total_sales_value')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_date')
    inlines = [BookImageInline]

    def total_sold(self, obj):
        # OrderItem dan shu kitob sotilgan miqdorini hisoblash
        total = OrderItem.objects.filter(book=obj).aggregate(total_sold=Sum('quantity'))['total_sold']
        return total if total else 0
    total_sold.short_description = 'Sotilgan soni'

    def total_sales_value(self, obj):
        # Umumiy sotuv price'sini hisoblash (total_quantity * price)
        total_value = OrderItem.objects.filter(
            book=obj).aggregate(total_sales=Sum(F('quantity') * F('book__price')))['total_sales']
        return total_value if total_value else 0
    total_sales_value.short_description = 'Sotilgan puli'

    def changelist_view(self, request, extra_context=None):
        # Sotilmay turgan kitoblarning umumiy narxini hisoblaymiz
        unsold_books_value = Book.objects.aggregate(
            total_unsold_value=Sum(F('stock') * F('price')))['total_unsold_value']

        # Jami sotilgan kitoblarning umumiy qiymatini hisoblash
        total_sold_books_value = OrderItem.objects.aggregate(
            total_sales=Sum(F('quantity') * F('book__price')))['total_sales']

        # Sotilgan kitoblarning umumiy sonini hisoblash
        total_sold_books_count = OrderItem.objects.aggregate(total_sold=Sum('quantity'))['total_sold']

        # Qolgan kitoblarning umumiy sonini hisoblash
        total_unsold_books_count = Book.objects.aggregate(total_unsold=Sum('stock'))['total_unsold']

        if extra_context is None:
            extra_context = {}
        extra_context['unsold_books_value'] = unsold_books_value or 0
        extra_context['total_sold_books_value'] = total_sold_books_value or 0
        extra_context['total_sold_books_count'] = total_sold_books_count or 0
        extra_context['total_unsold_books_count'] = total_unsold_books_count or 0

        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Book, BookAdmin)
admin.site.register(BookImage)
