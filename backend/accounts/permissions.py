from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """
    Classe-base de permissão por perfil. Não usar diretamente — usar as
    permissões já prontas abaixo (IsAdmin, IsAdvogado, etc.) ou criar
    novas com role_permission(...) nos próximos módulos.

    Superusuário sempre passa, independente do role, para facilitar
    administração/suporte.
    """

    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return user.is_superuser or user.role in self.allowed_roles


def role_permission(*roles: str) -> type[HasRole]:
    """Fábrica de classes de permissão para uma combinação de roles."""
    return type("RolePermission", (HasRole,), {"allowed_roles": roles})


# Permissões prontas para uso nos próximos módulos (clientes, processos, etc.)
IsAdmin = role_permission("admin")
IsAdvogado = role_permission("admin", "advogado")
IsSecretaria = role_permission("admin", "secretaria")
IsAdvogadoOuSecretaria = role_permission("admin", "advogado", "secretaria")
IsCliente = role_permission("cliente")
