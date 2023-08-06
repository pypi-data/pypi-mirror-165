from django import forms
from django.conf import settings
import logging

from django_filters import ModelChoiceFilter
from django_filters.fields import ModelChoiceField

from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, VLAN, VRF

from nautobot.utilities.forms import (
    BootstrapMixin, CSVModelForm, DynamicModelChoiceField,
    DynamicModelMultipleChoiceField, CSVModelChoiceField,
)
from .models import (
    AnycastIP, AnycastDummyIP, VRFPrimaryVLAN, VLANVRFList, EthernetSegmentMembership, EthernetSegment,
)

from .helper import get_unused_es_number

logger = logging.getLogger('nautobot.evpn')


class VRFPrimaryVLANForm(BootstrapMixin, forms.ModelForm):
    vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.exclude(pk__in=VRFPrimaryVLAN.objects.all().values_list('vlan_id', flat=True)),
        required=False,
        label='VLAN',
    )

    vrf = forms.ModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = VRFPrimaryVLAN
        fields = ('vlan', 'vrf')


class VLANAddToVRFForm(BootstrapMixin, forms.ModelForm):
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label='VRF',
    )

    vlan = forms.ModelChoiceField(
        queryset=VLAN.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = VLANVRFList
        fields = ('vlan', 'vrf')


class VLANAnycastIPForm(BootstrapMixin, forms.Form):
    vlan = forms.ModelChoiceField(
        queryset=VLAN.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput()
    )
    ips = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label='IPs',
        display_field='address',
    )
    dummy_ips = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label='IPs',
        display_field='address',
    )

    class Meta:
        fields = ('vlan', 'ips', 'dummy_ips')

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self):
        vlan = self.cleaned_data['vlan']

        # delete old state
        AnycastIP.objects.filter(vlan=vlan).delete()

        # delete old state
        AnycastDummyIP.objects.filter(vlan=vlan).delete()

        for ip in self.cleaned_data['ips']:
            AnycastIP(vlan=vlan, ip=ip).save()

        for dummy_ip in self.cleaned_data['dummy_ips']:
            AnycastDummyIP(vlan=vlan, ip=dummy_ip).save()


class JoinEthernetSegmentForm(BootstrapMixin, forms.ModelForm):
    segment = DynamicModelChoiceField(
        queryset=EthernetSegment.objects.all(),
        required=True,
        label='Ethernet Segment',
    )

    interface = forms.ModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = EthernetSegmentMembership
        fields = ('segment', 'interface')


class EthernetSegmentForm(BootstrapMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):

        if "initial" in kwargs:
            kwargs['initial']['segment_id'] = get_unused_es_number()

        super().__init__(*args, **kwargs)

    class Meta:
        model = EthernetSegment
        fields = ('segment_id', 'name')


class EthernetSegmentCSVForm(CSVModelForm):
    class Meta:
        model = EthernetSegment
        fields = EthernetSegment.csv_headers


class EthernetSegmentMembershipCSVForm(CSVModelForm):
    segment = CSVModelChoiceField(
        queryset=EthernetSegment.objects.all(),
        to_field_name='name',
        help_text='Ethernet Segment'
    )
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name='name',
        help_text='Device'
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        to_field_name='name',
        help_text='Interface',
    )

    class Meta:
        model = EthernetSegmentMembership
        fields = ["segment", "device", "interface"]

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        if data:
            # Limit interface queryset by assigned device
            params = {f"device__{self.fields['device'].to_field_name}": data.get('device')}
            self.fields['interface'].queryset = self.fields['interface'].queryset.filter(**params)
