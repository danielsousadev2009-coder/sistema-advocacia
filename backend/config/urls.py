from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/escritorios/", include("core.urls")),
    path("api/solicitacoes/", include("atendimento.urls")),
    path("api/clientes/", include("clientes.urls")),
    path("api/", include("processos.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-docs"),
    path("api/", include("agenda.urls")),
    path("api/", include("prazos.urls")),
    path("api/", include("documentos.urls")),
    path('api/dashboard/', include('dashboard.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)