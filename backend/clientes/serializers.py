from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    """CRUD de clientes (RF10). Uso por secretaria/admin/advogado."""

    tipo_pessoa_label = serializers.CharField(source="get_tipo_pessoa_display", read_only=True)

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nome",
            "email",
            "telefone",
            "tipo_pessoa",
            "tipo_pessoa_label",
            "cpf_cnpj",
            "endereco",
            "ativo",
            "criado_em",
            "solicitacao_origem",
        ]
        read_only_fields = ["id", "criado_em", "solicitacao_origem"]