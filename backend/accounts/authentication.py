from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    O simplejwt, por padrão, espera o access token no header
    "Authorization: Bearer <token>". Nós decidimos guardar o token em um
    cookie httpOnly em vez de localStorage (proteção contra roubo via
    XSS — ver decisão de arquitetura), então precisamos ler o token do
    cookie em vez do header.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get(settings.AUTH_COOKIE_ACCESS)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
