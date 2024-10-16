from rest_framework import serializers
from rest_framework import serializers
from .models import Transfer
from warehouse.models import Warehouse, WarehouseItem


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['from_warehouse', 'to_warehouse', 'from_warehouse_item', 'to_warehouse_item', 'book', 'count', 'status']

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'confirmed':
            instance.status = 'confirmed'
            instance.save()
        return instance

