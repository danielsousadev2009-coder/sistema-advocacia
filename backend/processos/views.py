from rest_framework import viewsets, permissions
from .models import Processo
from .serializers import ProcessoSerializer


class ProcessoViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Processo.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)