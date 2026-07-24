"""
Configuração do projeto Django.

Decisões arquiteturais desta etapa (autenticação):
- AUTH_USER_MODEL customizado (accounts.Usuario) desde o início, porque
  trocar o modelo de usuário depois de já existirem migrations/dados é
  extremamente doloroso no Django. Mais barato decidir isso agora.
- Autenticação via cookies httpOnly (não localStorage) — ver justificativa
  completa na conversa com o time de produto. Isso exige:
    * CORS_ALLOW_CREDENTIALS = True
    * Uma classe de autenticação customizada (accounts.authentication)
      que lê o token do cookie em vez do header Authorization padrão
      do simplejwt.
- Multi-tenant desde o schema (Escritorio como FK em Usuario), mesmo
  operando hoje com um único escritório, para não migrar depois.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "inseguro-troque-em-producao")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceiros
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    # Apps do projeto
    "core",
    "accounts",
    "atendimento",
    "clientes",
    'processos',
    'agenda',
    'prazos',
    'documentos',
    'dashboard'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # CorsMiddleware precisa vir antes do CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "gestao_juridica"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Modelo de usuário customizado — ver docstring do módulo.
AUTH_USER_MODEL = "accounts.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- Django REST Framework ----------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.CookieJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ---------- SimpleJWT ----------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ---------- Cookies de autenticação (nossa camada por cima do SimpleJWT) ----------
AUTH_COOKIE_ACCESS = "access_token"
AUTH_COOKIE_REFRESH = "refresh_token"
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 15          # 15 minutos, espelha ACCESS_TOKEN_LIFETIME
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 * 7  # 7 dias, espelha REFRESH_TOKEN_LIFETIME
# Em produção (HTTPS): defina AUTH_COOKIE_SECURE=True e AUTH_COOKIE_SAMESITE=None
AUTH_COOKIE_SECURE = os.environ.get("AUTH_COOKIE_SECURE", "False") == "True"
AUTH_COOKIE_SAMESITE = os.environ.get("AUTH_COOKIE_SAMESITE", "Lax")

# ---------- CORS ----------
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

# ---------- Documentação da API (schema OpenAPI para gerar tipos no frontend) ----------
SPECTACULAR_SETTINGS = {
    "TITLE": "API — Sistema de Gestão Jurídica",
    "DESCRIPTION": "Backend Django/DRF do SaaS jurídico multi-escritório.",
    "VERSION": "1.0.0",
}
