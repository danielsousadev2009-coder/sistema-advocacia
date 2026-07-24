from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Representa o usuário autenticado para o frontend (endpoint /me/ e
    resposta do /login/). Somente leitura — criação/edição de usuários
    é responsabilidade de um módulo futuro (Usuários/Configurações).
    """

    nome = serializers.CharField(source="get_full_name", read_only=True)
    role_label = serializers.CharField(source="get_role_display", read_only=True)
    escritorio_nome = serializers.CharField(source="escritorio.nome", read_only=True, default=None)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nome",
            "role",
            "role_label",
            "cargo",
            "telefone",
            "escritorio",
            "escritorio_nome",
        ]
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8, trim_whitespace=False)
