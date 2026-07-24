import uuid

from django.conf import settings
from django.db import models

from core.models import Escritorio
from clientes.models import Cliente
from processos.models import Processo


class SolicitacaoAtendimento(models.Model):
    """
    Pedido de atendimento feito por um cliente em potencial, através da
    área pública do site (RF01). Fica pendente até a secretaria analisar
    e aprovar ou recusar (RF07/RF08). Se aprovada, dá origem a um
    Usuario com role=cliente (módulo futuro fará essa conversão).
    """

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        APROVADA = "aprovada", "Aprovada"
        RECUSADA = "recusada", "Recusada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey(
        Escritorio,
        on_delete=models.CASCADE,
        related_name="solicitacoes",
    )

    # Dados informados pelo futuro cliente (RF01)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    area_juridica = models.CharField(max_length=100)
    descricao_caso = models.TextField()

    urgente = models.BooleanField(
        default=False,
        help_text="Se marcado, a aprovação já cria o cliente automaticamente, sem etapa manual.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    motivo_recusa = models.TextField(blank=True, default="")

    criado_em = models.DateTimeField(auto_now_add=True)
    analisado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Solicitação de atendimento"
        verbose_name_plural = "Solicitações de atendimento"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"


class Atendimento(models.Model):
    """
    Registro histórico de um atendimento já realizado a um cliente
    (presencial, online, telefone ou WhatsApp). Diferente da
    SolicitacaoAtendimento, que é o pré-cadastro público de quem ainda
    não é cliente — este model documenta contatos com clientes já
    existentes na base.
    """

    class Tipo(models.TextChoices):
        PRESENCIAL = "presencial", "Presencial"
        ONLINE = "online", "Online"
        TELEFONE = "telefone", "Telefone"
        WHATSAPP = "whatsapp", "WhatsApp"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey(
        Escritorio,
        on_delete=models.CASCADE,
        related_name="atendimentos",
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="atendimentos",
    )
    processo = models.ForeignKey(
        Processo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimentos",
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimentos_realizados",
    )

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    data_hora = models.DateTimeField()
    descricao = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
        ordering = ["-data_hora"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.cliente.nome} ({self.data_hora})"