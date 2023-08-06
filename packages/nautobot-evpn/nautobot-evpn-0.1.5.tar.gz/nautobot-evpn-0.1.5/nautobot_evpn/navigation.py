
from nautobot.extras.plugins import PluginMenuItem, PluginMenuButton
from nautobot.utilities.choices import ButtonColorChoices


menu_items = (
    PluginMenuItem(link='plugins:nautobot_evpn:es-list', link_text="Ethernet Segments", buttons=[
        PluginMenuButton('plugins:nautobot_evpn:es-add', "Add Ethernet Segment","mdi mdi-plus-thick", ButtonColorChoices.GREEN),
        PluginMenuButton('plugins:nautobot_evpn:es-import', "Import Ethernet Segments","mdi mdi-database-import-outline", ButtonColorChoices.BLUE),
        PluginMenuButton('plugins:nautobot_evpn:esm-import', "Import Ethernet Segment Membership", "mdi mdi-database-import-outline", ButtonColorChoices.YELLOW)
    ]),
)
