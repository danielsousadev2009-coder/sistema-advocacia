import uuid
from django.db import models
from django.conf import settings


class Processo(models.Model):
    class AreaJuridica(models.TextChoices):
        CIVEL = 'civel', 'Cível'
        TRABALHISTA = 'trabalhista', 'Trabalhista'
        CRIMINAL = 'criminal', 'Criminal'
        TRIBUTARIO = 'tributario', 'Tributário'
        FAMILIA = 'familia', 'Família'
        PREVIDENCIARIO = 'previdenciario', 'Previdenciário'
        EMPRESARIAL = 'empresarial', 'Empresarial'
        OUTRO = 'outro', 'Outro'

    class Status(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        AGUARDANDO = 'aguardando', 'Aguardando'
        SUSPENSO = 'suspenso', 'Suspenso'
        ARQUIVADO = 'arquivado', 'Arquivado'
        ENCERRADO = 'encerrado', 'Encerrado'

    class EtapaKanban(models.TextChoices):
        """
        Etapa operacional do fluxo de trabalho interno do escritório
        (independente do 'status' jurídico do processo, acima).
        Usada para montar o quadro Kanban.
        """
        NOVO_CLIENTE = 'novo_cliente', 'Novo Cliente'
        ATENDIMENTO = 'atendimento', 'Atendimento'
        DOCUMENTACAO = 'documentacao', 'Documentação'
        PROCESSO = 'processo', 'Processo'
        AUDIENCIA = 'audiencia', 'Audiência'
        FINALIZADO = 'finalizado', 'Finalizado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey(
        'core.Escritorio', on_delete=models.CASCADE, related_name='processos'
    )
    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.PROTECT, related_name='processos'
    )
    numero_processo = models.CharField(max_length=50, blank=True)
    area_juridica = models.CharField(max_length=20, choices=AreaJuridica.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVO)
    etapa_kanban = models.CharField(
        max_length=20, choices=EtapaKanban.choices, default=EtapaKanban.NOVO_CLIENTE
    )
    advogado_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='processos_responsavel',
        limit_choices_to={'role': 'advogado'}
    )
    comarca_vara = models.CharField(max_length=150, blank=True)
    valor_causa = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    descricao = models.TextField(blank=True)
    data_distribuicao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.numero_processo or 'Sem número'} - {self.cliente.nome}"