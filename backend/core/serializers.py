from rest_framework import serializers

from .models import Escritorio, Notificacao


class EscritorioSerializer(serializers.ModelSerializer):
    """
    CRUD de escritórios (tenants). Uso restrito a admins — ver
    core.views.EscritorioListCreateView / EscritorioDetailView.
    """

    class Meta:
        model = Escritorio
        fields = [
            "id", "nome", "slug", "ativo", "criado_em",
            "logo", "telefone", "endereco", "whatsapp",
            "instagram", "areas_atuacao",
        ]
        read_only_fields = ["id", "criado_em"]


class ConfiguracoesEscritorioSerializer(serializers.ModelSerializer):
    """
    RF21/RF22 — usado pelo próprio usuário logado para ver/editar os
    dados do escritório ao qual pertence (logo, endereço, redes sociais
    etc). Não permite trocar `slug` nem `ativo` — isso é reservado ao
    CRUD de admin em EscritorioListCreateView/EscritorioDetailView.
    """

    class Meta:
        model = Escritorio
        fields = [
            "id", "nome", "logo", "telefone", "endereco",
            "whatsapp", "instagram", "areas_atuacao", "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]


class PesquisaClienteSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    nome = serializers.CharField()
    cpf_cnpj = serializers.CharField()
    telefone = serializers.CharField()
    email = serializers.CharField()


class PesquisaProcessoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    numero_processo = serializers.CharField()
    descricao = serializers.CharField()
    status = serializers.CharField()


class PesquisaEventoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    titulo = serializers.CharField()
    tipo = serializers.CharField()
    data_hora_inicio = serializers.DateTimeField()


class PesquisaPrazoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    titulo = serializers.CharField()
    data_vencimento = serializers.DateTimeField()
    status = serializers.CharField()


class NotificacaoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = Notificacao
        fields = [
            "id", "tipo", "tipo_display", "titulo", "mensagem",
            "lida", "criado_em",
        ]
        read_only_fields = ["id", "tipo", "titulo", "mensagem", "criado_em"]