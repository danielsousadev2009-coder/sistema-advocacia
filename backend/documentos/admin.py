from django.contrib import admin
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'cliente', 'processo', 'enviado_por', 'criado_em']
    list_filter = ['categoria', 'escritorio']
    search_fields = ['nome', 'cliente__nome']   