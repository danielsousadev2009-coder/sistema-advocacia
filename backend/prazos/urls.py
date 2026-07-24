from rest_framework.routers import DefaultRouter
from .views import PrazoViewSet

router = DefaultRouter()
router.register(r'prazos', PrazoViewSet, basename='prazo')

urlpatterns = router.urls