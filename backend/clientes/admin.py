from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "tipo_pessoa", "escritorio", "ativo", "criado_em"]
    list_filter = ["tipo_pessoa", "ativo", "escritorio"]
    search_fields = ["nome", "email", "cpf_cnpj"]
    readonly_fields = ["id", "criado_em"]