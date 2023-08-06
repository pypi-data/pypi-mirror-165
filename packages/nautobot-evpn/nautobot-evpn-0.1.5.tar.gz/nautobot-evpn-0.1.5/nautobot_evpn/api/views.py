from .filters import EthernetSegmentFilterSet

from .serializers import EthernetSegmentSerializer

from django.conf import settings

from nautobot.core.api.views import ModelViewSet, APIRootView
from ..models import EthernetSegment

plugin_configuration = settings.PLUGINS_CONFIG['nautobot_evpn']


class EthernetSegmentsRootView(APIRootView):
    def get_view_name(self):
        return "Ethernet Segments"


class EthernetSegmentsViewSet(ModelViewSet):
    queryset = EthernetSegment.objects.all()
    serializer_class = EthernetSegmentSerializer
    filterset_class = EthernetSegmentFilterSet

