# dashboard/views.py
from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clientes.models import Cliente
from processos.models import Processo
from prazos.models import Prazo
from agenda.models import Evento
from atendimento.models import SolicitacaoAtendimento


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        escritorio = request.user.escritorio
        agora = timezone.now()
        limite_prazos = agora + timedelta(days=7)

        total_clientes_ativos = Cliente.objects.filter(
            escritorio=escritorio,
            ativo=True,
        ).count()

        processos_em_andamento = Processo.objects.filter(
            escritorio=escritorio,
            status='ativo',
        ).count()

        proximos_prazos = Prazo.objects.filter(
            escritorio=escritorio,
            data_vencimento__range=[agora, limite_prazos],
        ).order_by('data_vencimento')[:10]

        proximos_compromissos = Evento.objects.filter(
            escritorio=escritorio,
            data_hora_inicio__gte=agora,
        ).order_by('data_hora_inicio')[:10]

        solicitacoes_pendentes = SolicitacaoAtendimento.objects.filter(
            escritorio=escritorio,
            status='pendente',
        ).count()

        data = {
            'total_clientes_ativos': total_clientes_ativos,
            'processos_em_andamento': processos_em_andamento,
            'proximos_prazos': [
                {
                    'id': str(p.id),
                    'titulo': p.titulo,
                    'data_vencimento': p.data_vencimento,
                    'prioridade': p.prioridade,
                    'status': p.status,
                }
                for p in proximos_prazos
            ],
            'proximos_compromissos': [
                {
                    'id': str(e.id),
                    'titulo': e.titulo,
                    'tipo': e.tipo,
                    'data_hora_inicio': e.data_hora_inicio,
                    'data_hora_fim': e.data_hora_fim,
                    'local': e.local,
                }
                for e in proximos_compromissos
            ],
            'solicitacoes_pendentes': solicitacoes_pendentes,
        }

        return Response(data)