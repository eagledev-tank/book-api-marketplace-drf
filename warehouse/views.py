from django.shortcuts import render
from rest_framework import viewsets
from warehouse.models import Warehouse, WarehouseItem
from warehouse.serializers import WarehouseSerializer, WarehouseItemSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseItemViewSet(viewsets.ModelViewSet):
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer

