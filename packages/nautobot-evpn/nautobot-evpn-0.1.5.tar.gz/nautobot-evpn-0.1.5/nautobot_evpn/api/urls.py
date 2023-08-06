from django.urls import path

from nautobot.core.api import OrderedDefaultRouter
from .views import EthernetSegmentsViewSet

router = OrderedDefaultRouter()

router.register("ethernet-segments", EthernetSegmentsViewSet)

app_name = "nautobot_evpn-api"
urlpatterns = router.urls
