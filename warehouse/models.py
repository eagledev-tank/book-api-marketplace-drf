from django.db import models
from book.models import Book


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    count = models.IntegerField(default=0) # shu bazada nechta maxsulot bor
    total = models.DecimalField(max_digits=17, decimal_places=2, default=0) # shu bazada nechi pullik maxsulot borligi

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.total = sum(warehouseitem.total for warehouseitem in self.warehouse_item.all())
        self.count = sum(warehouseitem.count for warehouseitem in self.warehouse_item.all())
        super().save(*args, **kwargs)


class WarehouseItem(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouse_item', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=17, decimal_places=2)
    total = models.DecimalField(max_digits=17, decimal_places=2, default=0) # imenno shu maxsulotdan nechi pullik borligi, shu bazada

    def __str__(self):
        return self.book.title

    def save(self, *args, **kwargs):
        self.total = self.count * self.price
        super().save(*args, **kwargs)

        # Warehouse modelini ham yangilash
        self.warehouse.save()  # Warehouse ning total qiymatini yangilash uchun
