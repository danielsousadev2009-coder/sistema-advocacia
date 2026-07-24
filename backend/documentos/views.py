from rest_framework import viewsets, permissions, parsers
from .models import Documento
from .serializers import DocumentoSerializer


class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return Documento.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio, enviado_por=self.request.user)