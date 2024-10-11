from django.urls import path
from rest_framework import routers
from order.views import OrderModelViewSet, OrderItemModelViewSet, OrderStatusReportView

router = routers.SimpleRouter()

router.register(r'Orders', OrderModelViewSet, basename='order')
router.register(r'OrderItem', OrderItemModelViewSet, basename='order-items')


urlpatterns = [
    path('<str:status>/', OrderStatusReportView.as_view(), name='order-status-report'),
]
