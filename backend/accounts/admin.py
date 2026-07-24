from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PasswordResetToken, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "role", "escritorio", "is_active"]
    list_filter = ["role", "escritorio", "is_active"]
    search_fields = ["email", "first_name", "last_name"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name", "cargo", "telefone")}),
        ("Organização", {"fields": ("escritorio", "role")}),
        (
            "Permissões",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role", "escritorio"),
            },
        ),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ["usuario", "criado_em", "usado"]
    list_filter = ["usado"]
    search_fields = ["usuario__email"]
    readonly_fields = ["token", "criado_em"]
