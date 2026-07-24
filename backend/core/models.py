import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Escritorio(models.Model):
    """
    Representa um escritório de advocacia cliente do SaaS (tenant).

    Modelado desde a Etapa 1 mesmo operando hoje com um único escritório
    (Advocacia Neves), porque isolar dados por escritório depois de já
    existirem processos, clientes e documentos reais seria uma migração
    arriscada. Toda entidade sensível do sistema (Usuario, Cliente,
    Processo, etc.) deve referenciar Escritorio direta ou indiretamente.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Configurações (RF21/RF22)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True, default="")
    endereco = models.CharField(max_length=255, blank=True, default="")
    whatsapp = models.CharField(max_length=20, blank=True, default="")
    instagram = models.CharField(max_length=100, blank=True, default="")
    areas_atuacao = models.TextField(blank=True, default="")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Escritório"
        verbose_name_plural = "Escritórios"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Notificacao(models.Model):
    """
    Central de Notificações. Usa GenericForeignKey para referenciar de
    forma real o objeto de origem (Prazo, Evento, Cliente etc.), em vez
    de guardar um link em texto solto — assim a notificação continua
    íntegra mesmo se o sistema crescer e ganhar mais tipos de origem.

    `destinatario=None` significa notificação para todo o escritório
    (broadcast); se preenchido, é dirigida a um usuário específico.
    """

    class Tipo(models.TextChoices):
        PRAZO = "prazo", "Prazo"
        AUDIENCIA = "audiencia", "Audiência"
        NOVO_CLIENTE = "novo_cliente", "Novo cliente"
        GERAL = "geral", "Geral"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey(
        Escritorio, on_delete=models.CASCADE, related_name="notificacoes"
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="notificacoes"
    )

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)

    # Referência genérica ao objeto de origem (Prazo, Evento, Cliente...)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.UUIDField(null=True, blank=True)
    objeto_relacionado = GenericForeignKey("content_type", "object_id")

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"