import re
from .base import BaseDevice

VALID_PORTS = re.compile(r"^(ge|xe)-")

ADMIN_STATUS = {
    "up": "enabled",
    "down": "disabled",
}
OPER_STATUS = {"up": "up", "down": "down"}
DUPLEX = {
    "Half-duplex": "half",
    "Full-duplex": "full",
}
SPEED = {
    "Auto": "auto",
    "1000mbps": "1000",
    "100mbps": "100",
    "10mbps": "10",
}


class Junos(BaseDevice):
    def get_interface_details(self, interface=False):
        output = {}

        rpc = (
            self.device.rpc.jrpc__rpc_get_interface_information.get_interface_information
        )
        inp = rpc.get_input()

        self.log.info(f"interface is {interface}")

        # First we're getting interface information
        if interface:
            inp.interface_name = interface
        try:
            reply = rpc(inp)
        except:
            self.log.info(f"request failed")
            return []

        # save the fields we care about in our output as normalized data
        for i in reply.interface_information.physical_interface:

            self.log.info(f"processing port {i.name}")
            if not (VALID_PORTS.match(i.name)):
                continue

            if (not (interface)) or (interface and interface == i.name):
                output[i.name] = {
                    "admin_status": ADMIN_STATUS[i.admin_status],
                    "oper_status": OPER_STATUS[i.oper_status],
                    "speed": SPEED.get(i.speed, "auto"),
                    "duplex": DUPLEX.get(i.link_mode, "auto"),
                }

        return output

    def get_mac_table(self, mac=False):
        """
        Gathers mac address table data from a junos device
        and normalizes the output into a list. Each list entry is a dict
        with the interface name, vlan id, and mac address.
        """

        rpc = (
            self.device.rpc.jrpc__rpc_get_ethernet_switching_table_information.get_ethernet_switching_table_information
        )
        inp = rpc.get_input()
        inp.brief.create()
        if mac:
            mac = self.normalize_mac(mac)
            inp.address = mac
        try:
            reply = rpc(inp)
        except:
            return []

        mac_table = reply.l2ng_l2ald_rtb_macdb.l2ng_l2ald_mac_entry_vlan
        output = []

        if not (mac_table):
            return output
        else:
            mac_table = mac_table[0]

        for i in mac_table.l2ng_mac_entry:

            interface = i.l2ng_l2_mac_logical_interface.replace(".0", "")
            if not (VALID_PORTS.match(interface)):
                continue

            vlan_id = self.device.config.configuration.vlans.vlan[
                i.l2ng_l2_mac_vlan_name
            ].vlan_id
            address = i.l2ng_l2_mac_address

            if (not (mac)) or (mac and mac == address):
                output.append(
                    {
                        "interface": interface,
                        "vlan-id": vlan_id,
                        "address": address,
                    }
                )

        return output

    def get_arp_table(self, ip=False):

        rpc = (
            self.device.rpc.jrpc__rpc_get_arp_table_information.get_arp_table_information
        )
        inp = rpc.get_input()
        if ip:
            inp.hostname = ip

        try:
            reply = rpc(inp)
        except:
            return []

        output = []
        for a in reply.arp_table_information.arp_table_entry:

            if (not (ip)) or (ip and ip == a.ip_address):
                output.append(
                    {
                        "ip": a.ip_address,
                        "mac": a.mac_address,
                    }
                )

        return output


class Junos12(Junos):
    def get_mac_table(self, mac=False):
        """
        Gathers mac address table data from an old junos (12.x) device
        and normalizes the output into a list. Each list entry is a dict
        with the interface name, vlan id, and mac address.
        """

        rpc = (
            self.device.rpc.jrpc__rpc_get_ethernet_switching_table_information.get_ethernet_switching_table_information
        )
        inp = rpc.get_input()
        if mac:
            mac = self.normalize_mac(mac)
            inp.address = mac
        try:
            reply = rpc.get_ethernet_switching_table_information(inp)
        except:
            return []

        mac_table = (
            reply.ethernet_switching_table_information.ethernet_switching_table.mac_table_entry
        )

        output = []
        for mac in mac_table:

            interface = mac.mac_interfaces_list.mac_interfaces.replace(".0", "")
            if (mac.mac_type != "Learn") or not (VALID_PORTS.match(interface)):
                continue

            if not (mac) or (mac == mac.mac_address):
                output.append(
                    {
                        "interface": mac.mac_interfaces_list.mac_interfaces.replace(
                            ".0", ""
                        ),
                        "vlan-id": self.device.config.configuration.vlans.vlan[
                            mac.mac_vlan
                        ].vlan_id,
                        "address": mac.mac_address,
                    }
                )

        return output
