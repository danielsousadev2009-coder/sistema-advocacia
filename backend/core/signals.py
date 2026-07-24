from django.db.models.signals import post_save
from django.dispatch import receiver

from clientes.models import Cliente
from agenda.models import Evento

from .models import Notificacao


@receiver(post_save, sender=Cliente)
def notificar_novo_cliente(sender, instance, created, **kwargs):
    """Gera notificação automática quando um Cliente novo é cadastrado."""
    if not created:
        return
    Notificacao.objects.create(
        escritorio=instance.escritorio,
        tipo=Notificacao.Tipo.NOVO_CLIENTE,
        titulo="Novo cliente cadastrado",
        mensagem=f"{instance.nome} foi cadastrado(a) como cliente.",
        objeto_relacionado=instance,
    )


@receiver(post_save, sender=Evento)
def notificar_nova_audiencia(sender, instance, created, **kwargs):
    """Gera notificação automática quando um Evento do tipo audiência é criado."""
    if not created or instance.tipo != "audiencia":
        return
    Notificacao.objects.create(
        escritorio=instance.escritorio,
        tipo=Notificacao.Tipo.AUDIENCIA,
        titulo="Nova audiência agendada",
        mensagem=f"Audiência marcada: {instance.titulo}",
        objeto_relacionado=instance,
    )