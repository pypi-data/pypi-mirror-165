from django.db import models, transaction

from nautobot.core.models.generics import PrimaryModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, VLAN, VRF
from nautobot.utilities.querysets import RestrictedQuerySet


class VRFPrimaryVLAN(PrimaryModel):
    vlan = models.OneToOneField(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    vrf = models.OneToOneField(
        VRF,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "VRF Primary VLAN"
        verbose_name_plural = "VRF Primary VLANs"

    def __str__(self):
        return f'{self.vlan} in {self.vrf}'


class EthernetSegment(PrimaryModel):
    segment_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)

    csv_headers = ["segment_id", "name"]

    objects = RestrictedQuerySet.as_manager()

    @property
    def members(self):
        return EthernetSegmentMembership.objects.filter(segment=self).values_list("interface", flat=True)

    class Meta:
        verbose_name = "Ethernet Segment"
        verbose_name_plural = "Ethernet Segments"

    def __str__(self):
        return "{} ({})".format(self.name, self.segment_id)


class EthernetSegmentMembership(PrimaryModel):
    segment = models.ForeignKey(
        EthernetSegment,
        on_delete=models.CASCADE
    )
    interface = models.OneToOneField(
        Interface,
        on_delete=models.CASCADE
    )

    csv_headers = ["segment", "interface"]

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        verbose_name = "Ethernet Segment Membership"
        verbose_name_plural = "Ethernet Segment Memberships"

    def __str__(self):
        return f'{self.interface} in {self.segment}'


class VLANVRFList(PrimaryModel):
    vlan = models.OneToOneField(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    vrf = models.ForeignKey(
        VRF,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "VLAN-To-VRF-Attachment"
        verbose_name_plural = "VLAN-To-VRF-Attachments"

    def __str__(self):
        return f'{self.vrf} at {self.vlan}'


class AnycastIP(PrimaryModel):
    vlan = models.ForeignKey(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    ip = models.OneToOneField(
        IPAddress,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.ip} at {self.vlan}'


class AnycastDummyIP(PrimaryModel):
    vlan = models.ForeignKey(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    ip = models.OneToOneField(
        IPAddress,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.ip} at {self.vlan}'
