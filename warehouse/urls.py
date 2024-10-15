from django.urls import path
from .views import WarehouseViewSet, WarehouseItemViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('Warehouse', WarehouseViewSet, basename='Warehouse')
router.register('WarehouseItem', WarehouseItemViewSet, basename='WarehouseItem')

urlpatterns = [

]
