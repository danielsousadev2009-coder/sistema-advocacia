import uuid

from django.db import models

from accounts.models import Usuario
from core.models import Escritorio


class Cliente(models.Model):
    """
    Dados específicos de um cliente do escritório (pessoa física ou
    jurídica). Vinculado a um Usuario (para poder logar no sistema,
    role=cliente) e a um Escritorio (tenant). Pode ter se originado de
    uma SolicitacaoAtendimento aprovada, ou sido cadastrado diretamente
    pela secretaria/admin.
    """

    class TipoPessoa(models.TextChoices):
        FISICA = "fisica", "Pessoa física"
        JURIDICA = "juridica", "Pessoa jurídica"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey(
        Escritorio,
        on_delete=models.CASCADE,
        related_name="clientes",
    )
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="cliente",
        null=True,
        blank=True,
        help_text="Conta de login deste cliente. Pode ser nula até o acesso ser liberado.",
    )
    solicitacao_origem = models.ForeignKey(
        "atendimento.SolicitacaoAtendimento",
        on_delete=models.SET_NULL,
        related_name="cliente_gerado",
        null=True,
        blank=True,
    )

    tipo_pessoa = models.CharField(max_length=10, choices=TipoPessoa.choices, default=TipoPessoa.FISICA)
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18, blank=True, default="")
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, default="")
    endereco = models.CharField(max_length=255, blank=True, default="")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome