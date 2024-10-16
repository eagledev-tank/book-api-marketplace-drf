from django.contrib import admin
from .models import Warehouse, WarehouseItem


class WarehouseItemAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'book', 'count', 'price', 'total')
    list_filter = ('warehouse', 'book')
    readonly_fields = ('total',)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'total', 'count')
    readonly_fields = ('total',)


admin.site.register(WarehouseItem, WarehouseItemAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
