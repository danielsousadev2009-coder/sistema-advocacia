from rest_framework import serializers
from .models import Processo


class ProcessoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    area_juridica_label = serializers.CharField(source='get_area_juridica_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    etapa_kanban_label = serializers.CharField(source='get_etapa_kanban_display', read_only=True)
    advogado_nome = serializers.CharField(source='advogado_responsavel.nome', read_only=True, default='')

    class Meta:
        model = Processo
        fields = [
            'id', 'numero_processo', 'cliente', 'cliente_nome',
            'area_juridica', 'area_juridica_label',
            'status', 'status_label',
            'etapa_kanban', 'etapa_kanban_label',
            'advogado_responsavel', 'advogado_nome',
            'comarca_vara', 'valor_causa', 'descricao',
            'data_distribuicao', 'ativo', 'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_cliente(self, value):
        request = self.context.get('request')
        if request and value.escritorio_id != request.user.escritorio_id:
            raise serializers.ValidationError("Cliente não pertence ao seu escritório.")
        return value