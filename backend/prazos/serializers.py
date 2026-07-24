from rest_framework import serializers
from django.utils import timezone
from .models import Prazo


class PrazoSerializer(serializers.ModelSerializer):
    prioridade_label = serializers.CharField(source='get_prioridade_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True, default='')
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True, default='')
    dias_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Prazo
        fields = [
            'id', 'titulo', 'descricao', 'data_vencimento', 'dias_restantes',
            'processo', 'processo_numero',
            'responsavel', 'responsavel_nome',
            'prioridade', 'prioridade_label',
            'status', 'status_label', 'concluido_em',
            'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['id', 'concluido_em', 'criado_em', 'atualizado_em']

    def get_dias_restantes(self, obj):
        return (obj.data_vencimento - timezone.now().date()).days

    def validate_processo(self, value):
        request = self.context.get('request')
        if value and request and value.escritorio_id != request.user.escritorio_id:
            raise serializers.ValidationError("Processo não pertence ao seu escritório.")
        return value