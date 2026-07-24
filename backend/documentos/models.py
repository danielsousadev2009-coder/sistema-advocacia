import uuid
from django.db import models
from django.conf import settings


def documento_upload_path(instance, filename):
    return f"escritorio_{instance.escritorio_id}/cliente_{instance.cliente_id}/{filename}"


class Documento(models.Model):
    class Categoria(models.TextChoices):
        CONTRATO = 'contrato', 'Contrato'
        PROCURACAO = 'procuracao', 'Procuração'
        PETICAO = 'peticao', 'Petição'
        DOCUMENTO_PESSOAL = 'documento_pessoal', 'Documento Pessoal'
        COMPROVANTE = 'comprovante', 'Comprovante'
        OUTRO = 'outro', 'Outro'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escritorio = models.ForeignKey('core.Escritorio', on_delete=models.CASCADE, related_name='documentos')
    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.CASCADE, related_name='documentos'
    )
    processo = models.ForeignKey(
        'processos.Processo', on_delete=models.SET_NULL, related_name='documentos',
        null=True, blank=True
    )
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='documentos_enviados'
    )
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=30, choices=Categoria.choices, default=Categoria.OUTRO)
    arquivo = models.FileField(upload_to=documento_upload_path)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome