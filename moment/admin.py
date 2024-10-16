from django.contrib import admin
from .models import Transfer

class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_warehouse', 'to_warehouse', 'book', 'count', 'status')
    list_filter = ('status', 'from_warehouse', 'to_warehouse')
    search_fields = ('book__title',)  # Agar 'Book' modelida 'title' maydoni bo'lsa
    ordering = ('-id',)  # ID bo'yicha tartiblash, yoki boshqa mavjud maydonni qo'shishingiz mumkin

    # Qo'shimcha vaqt maydonlari uchun
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'confirmed':
            return ['from_warehouse', 'to_warehouse', 'book', 'count', 'status']
        return super().get_readonly_fields(request, obj)

# Transfer modelini admin interfeysida ro'yxatdan o'tkazish
admin.site.register(Transfer, TransferAdmin)
