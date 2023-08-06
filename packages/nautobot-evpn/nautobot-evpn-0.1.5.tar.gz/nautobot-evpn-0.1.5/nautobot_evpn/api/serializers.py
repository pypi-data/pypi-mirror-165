from nautobot.core.api import BaseModelSerializer
from ..models import EthernetSegment


class EthernetSegmentSerializer(BaseModelSerializer):

    class Meta:
        model = EthernetSegment
        fields = [
            "id",
            "name",
            "segment_id",
        ]
