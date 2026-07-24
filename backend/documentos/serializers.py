from rest_framework import serializers
from .models import Documento


class DocumentoSerializer(serializers.ModelSerializer):
    categoria_label = serializers.CharField(source='get_categoria_display', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True, default='')
    enviado_por_nome = serializers.CharField(source='enviado_por.nome', read_only=True, default='')

    class Meta:
        model = Documento
        fields = [
            'id', 'nome', 'categoria', 'categoria_label', 'arquivo',
            'cliente', 'cliente_nome', 'processo', 'processo_numero',
            'enviado_por', 'enviado_por_nome', 'descricao', 'criado_em',
        ]
        read_only_fields = ['id', 'enviado_por', 'criado_em']

    def validate_cliente(self, value):
        request = self.context.get('request')
        if request and value.escritorio_id != request.user.escritorio_id:
            raise serializers.ValidationError("Cliente não pertence ao seu escritório.")
        return value