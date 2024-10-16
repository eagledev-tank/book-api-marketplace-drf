from django.db import models
from django.utils.translation import gettext_lazy as _

from warehouse.models import WarehouseItem
from user.models import Profile


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),              # Buyurtma hali tasdiqlanmagan
        ('confirmed', _('Confirmed')),          # Buyurtma tasdiqlangan
        ('shipped', _('Shipped')),              # Buyurtma jo'natilgan
        ('delivered', _('Delivered')),          # Buyurtma qabul qilish punktiga yetkazilgan
        ('canceled', _('Canceled')),            # Buyurtma bekor qilingan
        ('completed', _('Completed')),          # Buyurtma bajarilgan
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)                        # Buyurtma bergan profile
    created_at = models.DateTimeField(auto_now_add=True)                                  # Buyurtma yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True)                                      # Buyurtma o'zgartirilgan vaqt
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')   # Buyurtma holati

    def __str__(self):
        return f"Order=> {self.id} - {self.profile.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)  # Buyurtma
    book = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE)                      # Kitob
    quantity = models.PositiveBigIntegerField(default=1)                                   # Kitoblar soni

    def __str__(self):
        return f"{self.quantity} x {self.book.book.title}"

    def save(self, *args, **kwargs):
        # Eski quantity'ni olish
        old_quantity = None
        if self.pk:  # Agar OrderItem mavjud bo'lsa (update jarayoni)
            old_quantity = OrderItem.objects.get(pk=self.pk).quantity

        new_quantity = self.quantity
        book = self.book

        # Kitobning mavjud miqdorini yangilash (eski va yangi quantity'ni taqqoslash)
        if old_quantity is not None:
            if new_quantity > old_quantity:
                # Agar yangi quantity katta bo'lsa, kitob stockidan farqni kamaytiramiz
                difference = new_quantity - old_quantity
                if book.count < difference:
                    raise ValueError(f'{book.book.title} dan {new_quantity} ta mavjud emas')
                book.count -= difference
            elif new_quantity < old_quantity:
                # Agar yangi quantity kichik bo'lsa, kitob stockiga farqni qaytaramiz
                difference = old_quantity - new_quantity
                book.count += difference
        else:
            # Yangi buyurtma bo'lsa, to'g'ridan-to'g'ri stockni kamaytiramiz
            if book.count < new_quantity:
                raise ValueError(f'{book.book.title} dan {new_quantity} ta mavjud emas')
            book.count -= new_quantity

        # Kitobning umumiy narxi (`total`) ni yangilash
        book.total = book.count * book.price
        book.save()

        # Asosiy save() metodini chaqirish
        super().save(*args, **kwargs)
