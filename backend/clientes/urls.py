from django.urls import path

from . import views

urlpatterns = [
    path("", views.ClienteListCreateView.as_view(), name="cliente-list-create"),
    path("<uuid:pk>/", views.ClienteDetailView.as_view(), name="cliente-detail"),
]