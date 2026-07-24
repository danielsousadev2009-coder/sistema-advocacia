from django.db.models import Q, Count
from django.utils import timezone
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin
from clientes.models import Cliente
from processos.models import Processo
from agenda.models import Evento
from atendimento.models import Atendimento
from prazos.models import Prazo

from .models import Escritorio, Notificacao
from .serializers import (
    EscritorioSerializer,
    ConfiguracoesEscritorioSerializer,
    PesquisaClienteSerializer,
    PesquisaProcessoSerializer,
    PesquisaEventoSerializer,
    PesquisaPrazoSerializer,
    NotificacaoSerializer,
)


class EscritorioListCreateView(ListCreateAPIView):
    """GET lista todos os escritórios / POST cria um novo. Só admin."""

    queryset = Escritorio.objects.all()
    serializer_class = EscritorioSerializer
    permission_classes = [IsAdmin]


class EscritorioDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE de um escritório específico. Só admin."""

    queryset = Escritorio.objects.all()
    serializer_class = EscritorioSerializer
    permission_classes = [IsAdmin]


class ConfiguracoesView(RetrieveUpdateAPIView):
    """
    RF21/RF22 — GET/PUT/PATCH dos dados do próprio escritório do
    usuário logado.
    """

    serializer_class = ConfiguracoesEscritorioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.escritorio


class PesquisaGlobalView(APIView):
    """
    Pesquisa Global — busca um termo simultaneamente em Clientes,
    Processos, Agenda (Eventos) e Prazos, sempre restrito ao
    escritório do usuário logado.

    GET /api/escritorios/pesquisa/?q=termo
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        termo = request.query_params.get("q", "").strip()
        escritorio = request.user.escritorio

        if not termo:
            return Response({
                "clientes": [],
                "processos": [],
                "eventos": [],
                "prazos": [],
            })

        clientes = Cliente.objects.filter(escritorio=escritorio).filter(
            Q(nome__icontains=termo)
            | Q(cpf_cnpj__icontains=termo)
            | Q(telefone__icontains=termo)
            | Q(email__icontains=termo)
        )[:20]

        processos = Processo.objects.filter(escritorio=escritorio).filter(
            Q(numero_processo__icontains=termo) | Q(descricao__icontains=termo)
        )[:20]

        eventos = Evento.objects.filter(escritorio=escritorio).filter(
            Q(titulo__icontains=termo) | Q(descricao__icontains=termo)
        )[:20]

        prazos = Prazo.objects.filter(escritorio=escritorio).filter(
            Q(titulo__icontains=termo) | Q(descricao__icontains=termo)
        )[:20]

        return Response({
            "clientes": PesquisaClienteSerializer(clientes, many=True).data,
            "processos": PesquisaProcessoSerializer(processos, many=True).data,
            "eventos": PesquisaEventoSerializer(eventos, many=True).data,
            "prazos": PesquisaPrazoSerializer(prazos, many=True).data,
        })


class EstatisticasView(APIView):
    """
    Estatísticas — números agregados de Clientes, Processos,
    Audiências (Eventos) e Atendimentos, restrito ao escritório do
    usuário logado.

    GET /api/escritorios/estatisticas/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        escritorio = request.user.escritorio
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        total_clientes = Cliente.objects.filter(escritorio=escritorio).count()
        clientes_ativos = Cliente.objects.filter(escritorio=escritorio, ativo=True).count()
        clientes_inativos = total_clientes - clientes_ativos

        processos_por_status = list(
            Processo.objects.filter(escritorio=escritorio)
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        processos_por_area = list(
            Processo.objects.filter(escritorio=escritorio)
            .values("area_juridica")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        eventos_por_tipo_mes = list(
            Evento.objects.filter(escritorio=escritorio, data_hora_inicio__gte=inicio_mes)
            .values("tipo")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        atendimentos_por_tipo_mes = list(
            Atendimento.objects.filter(escritorio=escritorio, data_hora__gte=inicio_mes)
            .values("tipo")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return Response({
            "clientes": {
                "total": total_clientes,
                "ativos": clientes_ativos,
                "inativos": clientes_inativos,
            },
            "processos": {
                "por_status": processos_por_status,
                "por_area_juridica": processos_por_area,
            },
            "eventos_mes_atual": eventos_por_tipo_mes,
            "atendimentos_mes_atual": atendimentos_por_tipo_mes,
        })


class NotificacaoListView(ListAPIView):
    """
    Lista as notificações do usuário logado: as dirigidas a ele
    diretamente + as de broadcast do escritório (destinatario=None).

    GET /api/escritorios/notificacoes/
    """

    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notificacao.objects.filter(escritorio=user.escritorio).filter(
            Q(destinatario=user) | Q(destinatario__isnull=True)
        )


class NotificacaoMarcarLidaView(APIView):
    """PATCH /api/escritorios/notificacoes/<uuid>/lida/ — marca como lida."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notificacao = Notificacao.objects.get(pk=pk, escritorio=request.user.escritorio)
        except Notificacao.DoesNotExist:
            return Response({"detail": "Notificação não encontrada."}, status=404)

        notificacao.lida = True
        notificacao.save()
        return Response(NotificacaoSerializer(notificacao).data)