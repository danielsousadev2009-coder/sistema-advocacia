from django.contrib import admin
from .models import Prazo


@admin.register(Prazo)
class PrazoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_vencimento', 'prioridade', 'status', 'responsavel', 'escritorio']
    list_filter = ['status', 'prioridade', 'escritorio']
    search_fields = ['titulo', 'processo__numero_processo']