from django.contrib import admin

from .models import SolicitacaoAtendimento


@admin.register(SolicitacaoAtendimento)
class SolicitacaoAtendimentoAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "area_juridica", "status", "criado_em"]
    list_filter = ["status", "escritorio"]
    search_fields = ["nome", "email"]
    readonly_fields = ["id", "criado_em"]