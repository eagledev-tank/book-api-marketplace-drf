from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import action
from rest_framework import status


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        """
        Buyurtma holatini 'confirmed' holatiga o'zgatiradi.
        """
        order = self.get_object()

        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            return Response({'status': 'Order confirmed'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Order cannot be confirmed'}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemModelViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
