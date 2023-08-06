import re
from typing import List, Dict, Any

from ntc_templates.parse import parse_output

from .base import BaseDevice

VALID_PORTS = re.compile(r"^Ethernet")
VALID_MAC = re.compile(r"[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}")

ADMIN_STATUS = {
    "connected": "enabled",
    "suspndByV": "enabled",
    "notconnec": "enabled",
    "disabled": "disabled",
    "sfpAbsent": "enabled",
    "xcvrAbsen": "enabled",
    "suspnd": "enabled",
    "suspended": "enabled",
}
OPER_STATUS = {
    "connected": "up",
    "suspndByV": "down",
    "notconnec": "down",
    "disabled": "down",
    "sfpAbsent": "down",
    "xcvrAbsen": "down",
    "suspnd": "down",
    "suspended": "down",
}
DUPLEX = {
    "half": "half",
    "full": "full",
    "auto": "full",
}
SPEED = {
    "10": "10",
    "100": "100",
    "1000": "1000",
    "auto": "auto",
    "a-10": "10",
    "a-100": "100",
    "a-1000": "1000",
    "a-10G": "10000",
}


class NXOS(BaseDevice):
    def _run_cmd(self, command: str) -> str:
        """
        use NCS live-status exec to issue a raw show command towards a device.
        platform-specific models are expected to parse this output and return
        structured data.

        :param command: string CLI command, e.g. 'show interface status'
        :returns: raw string output from the device
        """
        show = self.device.live_status.__getitem__("exec").show
        inp = show.get_input()
        inp.args = [command]

        return show.request(inp)

    def get_interface_details(self, interface=False) -> List[Dict]:
        """
        Gathers interface operational data from an NXOS device by parsing
        'show interfaces status'

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_interface_status
        """
        # ncs automatically adds the 'show' to the front of the cmd
        self.log.debug(f"sending 'show interface status' to {self.device.name}")
        command = f"interface {interface} status" if interface else "interface status"
        reply = self._run_cmd(command)
        self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        return parse_output(
            platform="cisco_nxos",
            command="show " + command,
            data=reply.result,
        )

    def get_bfd_neighbors(self) -> List:
        """
        Gathers bfd operational data from an NXOS device by parsing 'show bfd
        neighbors'

        see the ntc_templates test data for this template for details on output structure:
        https://gitlab.umich.edu/grundler/ntc-templates/-/tree/add-nxos-show-bfd-neighbors/tests/cisco_nxos/show_bfd_neighbors
        """
        self.log.debug(f"sending 'show bfd neighbors' to {self.device.name}")
        command = "bfd neighbors"
        reply = self._run_cmd(command)
        self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        return parse_output(
            platform="cisco_nxos",
            command="show " + command,
            data=reply.result,
        )

    def get_ospf_neighbors(self) -> List:
        """
        Gathers live ospf operational data from an NXOS device by parsing 'show
        ip ospf neighbor'

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_ip_ospf_neighbor
        """
        self.log.debug(f"sending 'show ip ospf neighbor' to {self.device.name}")
        command = "ip ospf neighbor"
        reply = self._run_cmd(command)
        self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        return parse_output(
            platform="cisco_nxos",
            command="show " + command,
            data=reply.result,
        )

    def get_lldp_neighbors(self) -> List:
        """
        Gathers live operational data about physically connected devices from an
        NXOS device by parsing 'show lldp neighbors'

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_lldp_neighbors
        """
        self.log.debug(f"sending 'show ip ospf neighbors' to {self.device.name}")
        command = "lldp neighbors"
        reply = self._run_cmd(command)
        self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        return parse_output(
            platform="cisco_nxos",
            command="show " + command,
            data=reply.result,
        )

    def get_transceiver_details(self) -> List:
        """
        Gathers live operational state DOM information from an NXOS device by
        parsing 'show interface tranceiver details'

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_interface_transceiver_details
        """
        self.log.debug(f"sending 'show ip ospf neighbors' to {self.device.name}")
        command = "interface transceiver details"
        reply = self._run_cmd(command)
        self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        return parse_output(
            platform="cisco_nxos",
            command="show " + command,
            data=reply.result,
        )

    def get_arp_table(self, ip=False):
        raise NotImplementedError

    def get_mac_table(self, mac=False):
        raise NotImplementedError
