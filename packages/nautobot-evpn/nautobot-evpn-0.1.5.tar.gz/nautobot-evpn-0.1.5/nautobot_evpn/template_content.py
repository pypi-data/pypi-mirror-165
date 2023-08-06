
from nautobot.dcim.choices import InterfaceTypeChoices
from nautobot.extras.plugins import PluginTemplateExtension
from nautobot.ipam.models import VRF

from .models import (
    VRFPrimaryVLAN, VLANVRFList, EthernetSegmentMembership, EthernetSegment,
    AnycastIP
)

class VRFPrimaryVLANConnect(PluginTemplateExtension):
    model = 'ipam.vrf'

    def buttons(self):
        vrf = self.context['object']
        vlanvrf = None
        try:
            vlanvrf = VRFPrimaryVLAN.objects.get(vrf=vrf)
        except VRFPrimaryVLAN.DoesNotExist:
            pass
        return self.render('nautobot_evpn/inc/vrf_buttons.html', {
            'vrf': vrf,
            'vlanvrf': vlanvrf,
        })


class VLANAddToVRF(PluginTemplateExtension):
    model = 'ipam.vlan'

    def buttons(self):
        vlan = self.context['object']
        vlanvrf = None
        try:
            vlanvrf = VLANVRFList.objects.get(vlan=vlan)
        except VLANVRFList.DoesNotExist:
            pass
        return self.render('nautobot_evpn/inc/vlan_buttons.html', {
            'vlan': vlan,
            'vlanvrf': vlanvrf,
        })

class InterfaceEthernetSegment(PluginTemplateExtension):
    model = 'dcim.interface'

    def buttons(self):
        interface = self.context['object']

        if interface.type != InterfaceTypeChoices.TYPE_LAG:
            return ""

        es_membership = None
        try:
            es_membership = EthernetSegmentMembership.objects.get(interface=interface)
        except EthernetSegmentMembership.DoesNotExist:
            pass

        return self.render('nautobot_evpn/inc/interface_buttons.html', {
            'interface': interface,
            'es_membership': es_membership,
        })

    def right_page(self):
        interface = self.context['object']

        if interface.type != InterfaceTypeChoices.TYPE_LAG:
            return ""

        es_membership = None
        try:
            es_membership = EthernetSegmentMembership.objects.get(interface=interface)
        except EthernetSegmentMembership.DoesNotExist:
            return ""

        es = es_membership.segment

        members = EthernetSegmentMembership.objects.filter(segment=es).exclude(interface=interface)

        if not members.exists():
            return ""

        return self.render('nautobot_evpn/inc/interface_es_widget.html', {
            'members': members,
            'es': es,
        })

class DeviceSVITemplate(PluginTemplateExtension):
    model = 'dcim.device'

    def collect_vlans(self, device):
        res = []
        for interface in device.interfaces.all():
            if interface.untagged_vlan:
                res.append(interface.untagged_vlan)
            res.extend(interface.tagged_vlans.all())
        return res

    def convert_vlans_to_svis(self, vlans):
        svis = []
        done = []
        for vlan in vlans:
            ips = AnycastIP.objects.filter(vlan=vlan)
            if ips.exists():
                svis.append({'vlan': vlan, 'ips': ips.values_list('ip__address', flat=True)})
                done.append(vlan)
        return svis, done

    def add_vrf_svis(self, vlans, done):
        svis = []
        vrf_ids = VLANVRFList.objects.filter(vlan__in=vlans).values_list('vrf_id', flat=True)
        vrfs = VRF.objects.filter(pk__in=vrf_ids).distinct().order_by()
        for vrf in vrfs:
            vlan = VRFPrimaryVLAN.objects.get(vrf=vrf).vlan
            if vlan not in vlans:
                svis.append({'vlan': vlan})
        return svis

    def full_width_page(self):
        device = self.context['object']

        if device.device_role.name != "leaf":
            return ""

        vlans = self.collect_vlans(device)

        svis, done = self.convert_vlans_to_svis(vlans)
        svis.extend(self.add_vrf_svis(vlans, done))

        if not svis:
            return ""

        return self.render('nautobot_evpn/inc/svi_widget.html', {
            'svis': svis,
        })

template_extensions = [
    VRFPrimaryVLANConnect, VLANAddToVRF, InterfaceEthernetSegment, DeviceSVITemplate
]
