from django.db import models
from warehouse.models import Warehouse, WarehouseItem
from book.models import Book


class Transfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    ]

    from_warehouse = models.ForeignKey(Warehouse, related_name='transfers_out', on_delete=models.PROTECT)
    to_warehouse = models.ForeignKey(Warehouse, related_name='transfers_in', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.status == 'confirmed':
            # from_warehouse dan WarehouseItem olish
            from_warehouse_item = WarehouseItem.objects.get(warehouse=self.from_warehouse, book=self.book)
            # to_warehouse dan WarehouseItem olish yoki yangi yaratish
            to_warehouse_item, created = WarehouseItem.objects.get_or_create(
                warehouse=self.to_warehouse,
                book=self.book,
                defaults={'count': 0, 'price': from_warehouse_item.price}
            )

            # Decrease from warehouse item's count and total
            from_warehouse_item.count -= self.count
            from_warehouse_item.total -= (from_warehouse_item.price * self.count)  # `total` maydoni yangilanadi
            from_warehouse_item.save()

            # Increase to warehouse item's count and total
            to_warehouse_item.count += self.count
            to_warehouse_item.total += (to_warehouse_item.price * self.count)  # `total` maydoni yangilanadi
            to_warehouse_item.save()

        super().save(*args, **kwargs)
