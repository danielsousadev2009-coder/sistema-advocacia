from rest_framework.routers import DefaultRouter
from .views import ProcessoViewSet

router = DefaultRouter()
router.register(r'processos', ProcessoViewSet, basename='processo')

urlpatterns = router.urls