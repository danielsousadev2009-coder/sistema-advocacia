from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Processo
from .serializers import ProcessoSerializer


class ProcessoViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Processo.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)

    @action(detail=False, methods=['get'], url_path='kanban')
    def kanban(self, request):
        """
        GET /api/processos/processos/kanban/

        Retorna os processos do escritório já agrupados por etapa,
        prontos para popular as colunas do quadro Kanban:

        {
            "novo_cliente": [...],
            "atendimento": [...],
            "documentacao": [...],
            "processo": [...],
            "audiencia": [...],
            "finalizado": [...]
        }
        """
        queryset = self.get_queryset().select_related('cliente', 'advogado_responsavel')
        serializer = self.get_serializer(queryset, many=True)

        colunas = {chave: [] for chave, _ in Processo.EtapaKanban.choices}
        for processo_data in serializer.data:
            colunas[processo_data['etapa_kanban']].append(processo_data)

        return Response(colunas)

    @action(detail=True, methods=['patch'], url_path='mover-etapa')
    def mover_etapa(self, request, pk=None):
        """
        PATCH /api/processos/processos/<uuid>/mover-etapa/
        Body: {"etapa_kanban": "documentacao"}

        Move o processo para outra etapa do Kanban (usado pelo
        drag-and-drop do quadro no frontend).
        """
        processo = self.get_object()
        nova_etapa = request.data.get('etapa_kanban')

        valores_validos = [chave for chave, _ in Processo.EtapaKanban.choices]
        if nova_etapa not in valores_validos:
            return Response(
                {'detail': f"Etapa inválida. Use uma de: {', '.join(valores_validos)}."},
                status=400,
            )

        processo.etapa_kanban = nova_etapa
        processo.save(update_fields=['etapa_kanban'])

        return Response(self.get_serializer(processo).data)