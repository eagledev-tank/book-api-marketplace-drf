from rest_framework import viewsets
from .models import Transfer
from .serializers import TransferSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'confirmed':
            instance.save()  # Trigger the warehouse updates on confirmed status
