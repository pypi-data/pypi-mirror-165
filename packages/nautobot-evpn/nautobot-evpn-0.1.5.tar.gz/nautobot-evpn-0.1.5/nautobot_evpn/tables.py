import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ButtonsColumn
from .models import (
    EthernetSegment,
    EthernetSegmentMembership
)


ACTIONS = """
<a href="{% url "plugins:nautobot_evpn:es-delete" pk=record.pk %}" class="btn btn-danger"> <i class="mdi mdi-trash-can-outline"></i></a>
"""




class EthernetSegmentTable(BaseTable):
    actions = tables.TemplateColumn(
        verbose_name='Actions',
        template_code=ACTIONS,
        orderable=False
    )

    class Meta(BaseTable.Meta):
        model = EthernetSegment
        fields = (
            "segment_id",
            "name",
            "actions"
        )


class EthernetSegmentMembershipTable(BaseTable):
    actions = tables.TemplateColumn(
        verbose_name='Actions',
        template_code=ACTIONS,
        orderable=False
    )

    class Meta(BaseTable.Meta):
        model = EthernetSegmentMembership
        fields = (
            "segment",
            "interface"
        )
