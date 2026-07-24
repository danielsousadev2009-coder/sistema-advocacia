from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Prazo
from .serializers import PrazoSerializer


class PrazoViewSet(viewsets.ModelViewSet):
    serializer_class = PrazoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prazo.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)

    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        prazo = self.get_object()
        prazo.status = Prazo.Status.CONCLUIDO
        prazo.concluido_em = timezone.now()
        prazo.save()
        return Response(self.get_serializer(prazo).data)