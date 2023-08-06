from __future__ import unicode_literals

from django.urls import path

from . import views

app_name = 'nautobot_evpn'
urlpatterns = [
    path(r'<uuid:pk>/vlan-link/add/', views.VRFPrimaryVLANView.as_view(), name='connect-vrf'),
    path(r'<uuid:pk>/vlan-link/delete/', views.VRFDisconnectPrimaryVLANView.as_view(), name='disconnect-vrf'),
    path(r'vrf-link/<uuid:pk>/add/', views.AddVRFView.as_view(), name='add-vrf'),
    path(r'vrf-link/<uuid:pk>/delete/', views.RemoveVRFView.as_view(), name='remove-vrf'),
    path(r'anycast-ips/<uuid:pk>/add/', views.VLANAnycastIPView.as_view(), name='anycast-ips'),
    path(r'es-link/<uuid:pk>/add/', views.JoinEthernetSegmentView.as_view(), name='join-es'),
    path(r'es-link/<uuid:pk>/delete/', views.LeaveEthernetSegmentView.as_view(), name='leave-es'),
    path(r'esm/import/', views.EthernetSegmentMembershipImportView.as_view(), name='esm-import'),
    path(r'es/', views.EthernetSegmentListView.as_view(), name='es-list'),
    path(r'es/add/', views.EthernetSegmentAddView.as_view(), name='es-add'),
    path(r'es/import/', views.EthernetSegmentImportView.as_view(), name='es-import'),
    path(r'es/<uuid:pk>/delete/', views.EthernetSegmentDeleteView.as_view(), name='es-delete'),
]
