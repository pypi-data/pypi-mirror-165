import django_filters
from django.db.models import Q

from ..models import EthernetSegment
from nautobot.utilities.filters import BaseFilterSet


class EthernetSegmentFilterSet(
    BaseFilterSet,
):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        model = EthernetSegment
        fields = ["id", "segment_id", "name"]


    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
        ).distinct()
