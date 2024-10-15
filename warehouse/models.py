from django.db import models
from book.models import Book


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=17, decimal_places=2) # shu bazada nechi pullik maxsulot borligi

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=17, decimal_places=2)
    total = models.DecimalField(max_digits=17, decimal_places=2) # imenno shu maxsulotdan nechi pullik borligi, shu bazada

    def __str__(self):
        return self.book.title
