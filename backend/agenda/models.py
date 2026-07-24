# agenda/models.py
import uuid
from django.db import models
from django.conf import settings


class Evento(models.Model):
    class Tipo(models.TextChoices):
        AUDIENCIA = 'audiencia', 'Audiência'
        REUNIAO = 'reuniao', 'Reunião'
        ATENDIMENTO = 'atendimento', 'Atendimento'
        PRAZO = 'prazo', 'Prazo'
        OUTRO = 'outro', 'Outro'

    class Status(models.TextChoices):
        AGENDADO = 'agendado', 'Agendado'
        REALIZADO = 'realizado', 'Realizado'
        CANCELADO = 'cancelado', 'Cancelado'
        REMARCADO = 'remarcado', 'Remarcado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey('core.Escritorio', on_delete=models.CASCADE, related_name='eventos')
    processo = models.ForeignKey(
        'processos.Processo', on_delete=models.CASCADE, related_name='eventos',
        null=True, blank=True
    )
    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.SET_NULL, related_name='eventos',
        null=True, blank=True
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='eventos_responsavel'
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    local = models.CharField(max_length=200, blank=True)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_hora_inicio']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"