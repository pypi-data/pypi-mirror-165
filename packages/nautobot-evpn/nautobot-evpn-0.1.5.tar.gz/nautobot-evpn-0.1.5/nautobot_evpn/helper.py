from .models import EthernetSegment
from django.db.models import Exists, OuterRef

def get_unused_es_number():
    previous_es = EthernetSegment.objects.filter(
        ~Exists(EthernetSegment.objects.filter(segment_id=OuterRef('segment_id') + 1)),
    ).order_by("segment_id").first()

    if not previous_es:
        return 1

    return previous_es.segment_id + 1
