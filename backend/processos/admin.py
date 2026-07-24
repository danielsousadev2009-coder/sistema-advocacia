from django.contrib import admin
from .models import Processo


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ['numero_processo', 'cliente', 'area_juridica', 'status', 'advogado_responsavel', 'escritorio']
    list_filter = ['status', 'area_juridica', 'escritorio']
    search_fields = ['numero_processo', 'cliente__nome']