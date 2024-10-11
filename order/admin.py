from django.contrib import admin
from order.models import Order, OrderItem


class StockManager:
    @staticmethod
    def update_book_stock(book, old_quantity, new_quantity):
        """Kitob zaxirasini eski va yangi quantity asosida yangilaydi."""
        if new_quantity > old_quantity:
            difference = new_quantity - old_quantity
            if book.stock < difference:
                raise ValueError(f"{book.title} dan {difference} ta mavjud emas")
            book.stock -= difference
        elif new_quantity < old_quantity:
            difference = old_quantity - new_quantity
            book.stock += difference
        book.save()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('get_total_item_price',)
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'status', 'get_books', 'created_at', 'updated_at', 'get_total_price')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('profile__user__email', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

    def get_books(self, obj):
        return obj.get_books()  # `obj` argumenti beriladi
    get_books.short_description = 'Books with Prices and Quantities'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        if response.context_data:
            queryset = self.get_queryset(request)
            total_sum = sum(order.get_total_price() for order in queryset)
            response.context_data['total_sum'] = total_sum  # Yig'indini kontekstga qo'shamiz
        return response

    def total_sum_display(self, obj):
        """Umumiy narxlarni ko'rsatish uchun yordamchi metod."""
        return self.total_sum

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        order = form.instance
        for item in order.orderitems.all():
            old_quantity = 0  # Yangi yaratilgan buyurtmalar uchun default qiymat
            if change and item.pk:  # Agar yangilanayotgan bo'lsa
                old_item = OrderItem.objects.filter(pk=item.pk).first()
                if old_item:
                    old_quantity = old_item.quantity
            # Zaxirani yangilash
            StockManager.update_book_stock(item.book, old_quantity, item.quantity)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'get_total_item_price')
    search_fields = ('order__id', 'book__title')
    readonly_fields = ('get_total_item_price',)

    def get_total_item_price(self, obj):
        return obj.get_total_item_price()
    get_total_item_price.short_description = 'Item Total Price'

    def save_model(self, request, obj, form, change):
        book = obj.book
        new_quantity = obj.quantity

        old_quantity = 0  # Yangi buyurtmalar uchun default qiymat
        if change and obj.pk:  # Agar yangilanayotgan bo'lsa
            old_obj = OrderItem.objects.get(pk=obj.pk)
            old_quantity = old_obj.quantity

        # Zaxirani yangilash
        StockManager.update_book_stock(book, old_quantity, new_quantity)

        # Asl saqlash funksiyasini chaqirish
        super().save_model(request, obj, form, change)
