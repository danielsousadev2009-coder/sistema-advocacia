from django.contrib import admin

from .models import Escritorio


@admin.register(Escritorio)
class EscritorioAdmin(admin.ModelAdmin):
    list_display = ["nome", "slug", "ativo", "criado_em"]
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ["nome", "slug"]
