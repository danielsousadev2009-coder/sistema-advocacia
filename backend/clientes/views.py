from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.permissions import IsAdvogadoOuSecretaria

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteListCreateView(ListCreateAPIView):
    """GET lista clientes / POST cadastra um novo (RF10)."""

    serializer_class = ClienteSerializer
    permission_classes = [IsAdvogadoOuSecretaria]

    def get_queryset(self):
        return Cliente.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)


class ClienteDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE de um cliente específico (RF10)."""

    serializer_class = ClienteSerializer
    permission_classes = [IsAdvogadoOuSecretaria]

    def get_queryset(self):
        return Cliente.objects.filter(escritorio=self.request.user.escritorio)