from django.urls import path

from . import views

urlpatterns = [
    path("", views.EscritorioListCreateView.as_view(), name="escritorio-list-create"),
    path("<uuid:pk>/", views.EscritorioDetailView.as_view(), name="escritorio-detail"),
    path("configuracoes/", views.ConfiguracoesView.as_view(), name="configuracoes"),
    path("pesquisa/", views.PesquisaGlobalView.as_view(), name="pesquisa-global"),
    path("estatisticas/", views.EstatisticasView.as_view(), name="estatisticas"),
    path("notificacoes/", views.NotificacaoListView.as_view(), name="notificacao-list"),
    path("notificacoes/<uuid:pk>/lida/", views.NotificacaoMarcarLidaView.as_view(), name="notificacao-marcar-lida"),
]