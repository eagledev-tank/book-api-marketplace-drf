from django.db import models
from django.utils.translation import gettext_lazy as _

from book.models import Book
from user.models import Profile


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),              # Buyurtma hali tasdiqlanmagan
        ('confirmed', _('Confirmed')),          # Buyurtma tasdiqlangan
        ('shipped', _('Shipped')),              # Buyurtma jo'natilgan
        ('delivered', _('Delivered')),          # Buyurtma yetkazilgan
        ('canceled', _('Canceled')),            # Buyurtma bekor qilingan
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)                        # Buyurtma bergan profile
    created_at = models.DateTimeField(auto_now_add=True)                                  # Buyurtma yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True)                                      # Buyurtma o'zgartirilgan vaqt
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')   # Buyurtma holati

    def __str__(self):
        return f"Order {self.id} - {self.profile.user.email}"

    def get_total_price(self):
        """Buyurtmaning umumiy narxini hisoblaydi."""
        total = sum(item.get_total_item_price() for item in self.orderitems.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)  # Buyurtma
    book = models.ForeignKey(Book, on_delete=models.CASCADE)                               # Kitob
    quantity = models.PositiveBigIntegerField(default=1)                                   # Kitoblar soni

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_total_item_price(self):
        """Ushbu kitobning jami narxini hisoblaydi."""
        return self.quantity * self.book.price
