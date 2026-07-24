import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import UsuarioManager


class Role(models.TextChoices):
    """
    Os 4 perfis de permissão do sistema. Isto é o que controla acesso —
    não confundir com o campo `cargo` do Usuario, que é só um texto de
    exibição (ex: "Advogada Sênior", "Sócio-fundador") sem efeito em
    permissões.
    """

    ADMIN = "admin", "Administrador"
    ADVOGADO = "advogado", "Advogado"
    SECRETARIA = "secretaria", "Secretária"
    CLIENTE = "cliente", "Cliente"


class Usuario(AbstractUser):
    """
    Modelo de usuário customizado, substituindo o User padrão do Django
    desde o início do projeto (trocar depois exigiria migração manual
    complexa com dados reais já existentes).

    Login é feito por e-mail, não por username — por isso username=None
    e USERNAME_FIELD="email".
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField("e-mail", unique=True)

    escritorio = models.ForeignKey(
        "core.Escritorio",
        on_delete=models.CASCADE,
        related_name="usuarios",
        null=True,
        blank=True,
        help_text="Escritório ao qual este usuário pertence (tenant).",
    )
    role = models.CharField(
        "perfil de acesso",
        max_length=20,
        choices=Role.choices,
        help_text="Controla permissões. Não confundir com 'cargo'.",
    )
    cargo = models.CharField(
        "cargo (exibição)",
        max_length=100,
        blank=True,
        default="",
        help_text='Texto livre exibido na interface, ex: "Advogada Sênior". Não afeta permissões.',
    )
    telefone = models.CharField(max_length=20, blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        nome = self.get_full_name() or self.email
        return f"{nome} ({self.get_role_display()})"


class PasswordResetToken(models.Model):
    """
    Token de uso único para o fluxo de recuperação de senha.
    Expira em 1 hora e é invalidado após o primeiro uso.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=255, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Token de recuperação de senha"
        verbose_name_plural = "Tokens de recuperação de senha"

    def esta_valido(self):
        expiracao = self.criado_em + timedelta(hours=1)
        return not self.usado and timezone.now() < expiracao
