from rest_framework.routers import DefaultRouter

from .views import RestauranteViewSet

router = DefaultRouter()
router.register("", RestauranteViewSet, basename="restaurante")

urlpatterns = router.urls
