import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PasswordResetToken, Usuario
from .serializers import (
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    UsuarioSerializer,
)


def _set_auth_cookies(response: Response, user: Usuario) -> Response:
    """
    Gera o par access/refresh token e os grava como cookies httpOnly.
    O cookie de refresh é restrito ao path do endpoint de refresh, para
    reduzir a exposição do token de longa duração.
    """
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response.set_cookie(
        settings.AUTH_COOKIE_ACCESS,
        str(access),
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )
    response.set_cookie(
        settings.AUTH_COOKIE_REFRESH,
        str(refresh),
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/api/auth/refresh/",
    )
    return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["email"],  # USERNAME_FIELD = email
            password=serializer.validated_data["password"],
        )

        if user is None or not user.is_active:
            return Response(
                {"detail": "E-mail ou senha inválidos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(UsuarioSerializer(user).data, status=status.HTTP_200_OK)
        return _set_auth_cookies(response, user)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.AUTH_COOKIE_ACCESS, path="/")
        response.delete_cookie(settings.AUTH_COOKIE_REFRESH, path="/api/auth/refresh/")
        return response


class RefreshView(APIView):
    """
    Renova o access token usando o refresh token guardado no cookie.
    O frontend chama isso silenciosamente quando o access token expira
    (ex: interceptor de resposta 401 no cliente HTTP).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        raw_refresh = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
        if raw_refresh is None:
            return Response({"detail": "Sessão expirada."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(raw_refresh)
            new_access = refresh.access_token
        except TokenError:
            return Response({"detail": "Sessão inválida ou expirada."}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            settings.AUTH_COOKIE_ACCESS,
            str(new_access),
            max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            httponly=True,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path="/",
        )
        return response


class MeView(APIView):
    """
    Usado pelo router do frontend (beforeLoad) para saber quem está
    logado e qual o seu role, antes de renderizar rotas protegidas.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            usuario = Usuario.objects.get(email__iexact=email, is_active=True)
        except Usuario.DoesNotExist:
            # Não revelamos se o e-mail existe ou não — resposta 200 sempre,
            # para não permitir enumeração de contas.
            return Response(status=status.HTTP_200_OK)

        token = secrets.token_urlsafe(48)
        PasswordResetToken.objects.create(usuario=usuario, token=token)

        # TODO (próxima etapa de infraestrutura): disparar e-mail real.
        # Por enquanto, o link fica no console/log do servidor para testes.
        print(f"[reset-password] link para {usuario.email}: /reset-password?token={token}")

        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reset_token = PasswordResetToken.objects.select_related("usuario").get(
                token=serializer.validated_data["token"]
            )
        except PasswordResetToken.DoesNotExist:
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_token.esta_valido():
            return Response(
                {"detail": "Token expirado ou já utilizado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        usuario = reset_token.usuario
        usuario.set_password(serializer.validated_data["password"])
        usuario.save(update_fields=["password"])

        reset_token.usado = True
        reset_token.save(update_fields=["usado"])

        return Response(status=status.HTTP_200_OK)
