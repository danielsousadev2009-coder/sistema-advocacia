from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("atendimentos", views.AtendimentoViewSet, basename="atendimento")

urlpatterns = [
    path("", views.SolicitacaoCreateView.as_view(), name="solicitacao-create"),
    path("lista/", views.SolicitacaoListView.as_view(), name="solicitacao-list"),
    path("<uuid:pk>/aprovar/", views.SolicitacaoAprovarView.as_view(), name="solicitacao-aprovar"),
    path("<uuid:pk>/recusar/", views.SolicitacaoRecusarView.as_view(), name="solicitacao-recusar"),
    path("", include(router.urls)),
]