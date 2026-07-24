from rest_framework import serializers
from .models import Evento


class EventoSerializer(serializers.ModelSerializer):
    tipo_label = serializers.CharField(source='get_tipo_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True, default='')
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True, default='')
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True, default='')

    class Meta:
        model = Evento
        fields = [
            'id', 'tipo', 'tipo_label', 'titulo', 'descricao', 'local',
            'processo', 'processo_numero', 'cliente', 'cliente_nome',
            'responsavel', 'responsavel_nome',
            'data_hora_inicio', 'data_hora_fim',
            'status', 'status_label', 'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_cliente(self, value):
        request = self.context.get('request')
        if value and request and value.escritorio_id != request.user.escritorio_id:
            raise serializers.ValidationError("Cliente não pertence ao seu escritório.")
        return value

    def validate_processo(self, value):
        request = self.context.get('request')
        if value and request and value.escritorio_id != request.user.escritorio_id:
            raise serializers.ValidationError("Processo não pertence ao seu escritório.")
        return value