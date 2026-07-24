from rest_framework import serializers

from .models import Atendimento, SolicitacaoAtendimento


class SolicitacaoCreateSerializer(serializers.ModelSerializer):
    """RF01 — usado no endpoint público de criação de solicitação."""

    class Meta:
        model = SolicitacaoAtendimento
        fields = [
            'nome', 'email', 'telefone', 'area_juridica',
            'descricao_caso', 'urgente',
        ]


class SolicitacaoSerializer(serializers.ModelSerializer):
    """RF07/RF08 — usado para listar, aprovar e recusar solicitações."""

    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SolicitacaoAtendimento
        fields = [
            'id', 'escritorio', 'nome', 'email', 'telefone', 'area_juridica',
            'descricao_caso', 'urgente', 'status', 'status_display',
            'motivo_recusa', 'criado_em', 'analisado_em',
        ]
        read_only_fields = ['id', 'escritorio', 'criado_em', 'analisado_em']


class AtendimentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Atendimento
        fields = [
            'id', 'escritorio', 'cliente', 'cliente_nome', 'processo',
            'responsavel', 'responsavel_nome', 'tipo', 'tipo_display',
            'data_hora', 'descricao', 'criado_em',
        ]
        read_only_fields = ['id', 'escritorio', 'criado_em']