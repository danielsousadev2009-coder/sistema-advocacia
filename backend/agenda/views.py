from rest_framework import viewsets, permissions
from .models import Evento
from .serializers import EventoSerializer


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Evento.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)