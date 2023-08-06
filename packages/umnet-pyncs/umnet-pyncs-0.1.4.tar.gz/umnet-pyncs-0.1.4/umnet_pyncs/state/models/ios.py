import re
from .base import BaseDevice

VALID_PORTS = re.compile(r"^(Fa|Gi|Te)")
VALID_MAC = re.compile(r"[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}")

# note that since we're using 'show int status',
# admin and oper status leverage the same output column, whose values can be
## connected (admin up, oper up)
## notconnect (admin up, oper down)
## disabled (admin down, oper down)
## suspended (admin up, oper down)
## err-disabled (admin up, oper down)
ADMIN_STATUS = {
    "connected": "enabled",
    "notconnect": "enabled",
    "disabled": "disabled",
    "suspended": "enabled",
    "err-disabled": "enabled",
}
OPER_STATUS = {
    "connected": "up",
    "notconnect": "down",
    "disabled": "down",
    "suspended": "down",
    "err-disabled": "down",
}
DUPLEX = {
    "half": "half",
    "full": "full",
    "auto": "full",
    "a-half": "half",
    "a-full": "full",
}
SPEED = {
    "10": "10",
    "100": "100",
    "1000": "1000",
    "auto": "auto",
    "a-10": "10",
    "a-100": "100",
    "a-1000": "1000",
}


class IOS(BaseDevice):
    def get_interface_details(self, interface=False):
        """
        Gathers interface operational data from an ios device by parsing
        'show interfaces status'

        If you provide an interface name to the function it will
        only return data found for that interface.
        """
        show = self.device.live_status.__getitem__("exec").show
        inp = show.get_input()
        inp.args = (
            [f"interfaces {interface} status"] if interface else ["interfaces status"]
        )
        reply = show.request(inp)

        output = {}
        for line in reply.result.split("\n"):

            i_name = line[0:10].rstrip()
            if not (VALID_PORTS.match(i_name)):
                continue

            if (not (interface)) or (interface and interface == i_name):
                output[i_name] = {
                    "admin_status": ADMIN_STATUS[line[29:42].strip()],
                    "oper_status": OPER_STATUS[line[29:42].strip()],
                    "speed": SPEED[line[60:67].strip()],
                    "duplex": DUPLEX[line[53:60].strip()],
                }

        return output

    def get_arp_table(self, ip=False):
        """
        Gathers arp data from an ios device
        """
        show = self.device.live_status.__getitem__("exec").show
        inp = show.get_input()
        output = []

        # first we'll look in the main table
        inp.args = [f"ip arp {ip}"] if ip else [f"ip arp"]
        inp = show.get_input()
        reply = show.request(inp)
        output.extend(self._parse_arp_reply(reply, ip))

        # Now we'll look in all the vrfs - ios makes you run a separate
        # lookup command for every vrf (so rude)
        vrfs = [vrf.name for vrf in self.device.config.vrf.definition]
        for vrf in vrfs:
            inp.args = [f"ip arp vrf {vrf} {ip}"] if ip else [f"ip arp vrf {vrf}"]
            reply = show.request(inp)
            output.extend(self._parse_arp_reply(reply, ip))

        return output

    def get_mac_table(self, mac=False):
        """
        Parses mac address table data from an ios device
        """
        show = self.device.live_status.__getitem__("exec").show
        inp = show.get_input()
        if mac:
            inp.args = [f"mac address-table address {mac}"]
        else:
            inp.args = ["mac address-table dynamic"]
        reply = show.request(inp)

        self.log.info(f"results {reply.result}")
        output = []
        for line in reply.result.split("\n"):

            interface = line[38:46].strip()
            self.log.info(f"interface {interface}")
            if not (VALID_PORTS.match(interface)):
                continue

            vlan_id = line[0:8].strip()
            address = line[8:26].strip()

            # TODO: fix mac comparison
            if (not (mac)) or (mac and mac == self.normalize_mac(address)):
                output.append(
                    {
                        "interface": interface,
                        "vlan-id": vlan_id,
                        "address": self.normalize_mac(address),
                    }
                )

        return output

    def _parse_arp_reply(self, reply, ip):

        for line in reply.result.split("\n"):

            arp_ip = line[10:35].strip()
            arp_mac = line[38:52].strip()

            if not (VALID_MAC.match(arp_mac)):
                continue

            if (not (ip)) or (ip and arp_ip == ip):
                output.append(
                    {
                        "mac": arp_mac,
                        "ip": arp_ip,
                    }
                )

        return output
