# prazos/models.py
import uuid
from django.db import models
from django.conf import settings


class Prazo(models.Model):
    class Prioridade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'
        URGENTE = 'urgente', 'Urgente'

    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONCLUIDO = 'concluido', 'Concluído'
        PERDIDO = 'perdido', 'Perdido'
        CANCELADO = 'cancelado', 'Cancelado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey('core.Escritorio', on_delete=models.CASCADE, related_name='prazos')
    processo = models.ForeignKey(
        'processos.Processo', on_delete=models.CASCADE, related_name='prazos',
        null=True, blank=True
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='prazos_responsavel'
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_vencimento = models.DateField()
    prioridade = models.CharField(max_length=20, choices=Prioridade.choices, default=Prioridade.MEDIA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    concluido_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_vencimento']

    def __str__(self):
        return f"{self.titulo} - vence em {self.data_vencimento}"