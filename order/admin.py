from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'status', 'created_at', 'updated_at', 'get_books', 'get_total_price')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('profile__user__email', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def get_books(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        books = ', '.join([f"{order_item.quantity} x {order_item.book.book.title}" for order_item in order_items])
        return books

    get_books.short_description = 'Books'

    def get_total_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        return sum(order_item.quantity * order_item.book.price for order_item in order_items)

    get_total_price.short_description = 'Order total price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity')
    search_fields = ('order__id', 'book__title')
