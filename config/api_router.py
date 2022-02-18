from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from api_atelier.clients.api.views import ClientsViewSet, OrderViewSet, ServiceViewSet
from api_atelier.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("clients", ClientsViewSet, basename="clients")
router.register("services", ServiceViewSet, basename="services")
router.register("orders", OrderViewSet, basename="orders")


app_name = "api"
urlpatterns = router.urls
