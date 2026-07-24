from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'data_hora_inicio', 'status', 'cliente', 'processo', 'escritorio']
    list_filter = ['tipo', 'status', 'escritorio']
    search_fields = ['titulo', 'cliente__nome', 'processo__numero_processo']