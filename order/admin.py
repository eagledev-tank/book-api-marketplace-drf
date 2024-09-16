from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1   # Yangi buyurtmaga qo'shiladigan bo'sh satrlar soni
    readonly_fields = ('get_total_item_price',)
    can_delete = False  # Buyurtmadagi itemlarni o'chirishni cheklash


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'status', 'created_at', 'updated_at', 'get_total_price') # Admin ro'yxatida ko'rsatiladigan maydonlar
    list_filter = ('status', 'created_at', 'updated_at') # Filtrlar
    search_fields = ('profile__user__email', 'id')  # Qidiruv maydonlari
    inlines = [OrderItemInline]     # Order elementlarini inline qilib ko'rsatish
    readonly_fields = ('created_at', 'updated_at', 'get_total_price')  # Faqat o'qish uchun maydonlar

    def get_total_price(self, obj):
        """Buyurtmaning umumiy narxini ko'rsatadi."""
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'   # Maydon nomi


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'get_total_item_price')
    search_fields = ('order__id', 'book__title')    # Qidiruv maydonlari
    readonly_fields = ('get_total_item_price',)     # Faqat o'qish uchun maydonlar

    def get_total_item_price(self, obj):
        """Ushbu buyurtma elementining jami narxini ko'rsatadi."""
        return obj.get_total_item_price()
    get_total_item_price.short_description = 'Item Total Price' # Maydon nomi
