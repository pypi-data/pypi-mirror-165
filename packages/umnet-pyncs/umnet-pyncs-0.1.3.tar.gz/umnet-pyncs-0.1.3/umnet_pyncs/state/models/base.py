import re
import logging
from typing import Any

import ncs


class BaseDevice:
    def __init__(self, device: ncs.maagic.Node, log: logging.Logger):
        self.device = device
        self.log = log

    @staticmethod
    def normalize_mac(mac: str) -> str:
        mac = re.sub(r"[\.\-\:]", "", mac)
        return f"{mac[0:2]}:{mac[2:4]}:{mac[4:6]}:{mac[6:8]}:{mac[8:10]}:{mac[10:12]}"

    def _run_cmd(self, command: str) -> Any:
        raise NotImplementedError

    def get_mac_table(self, mac=False) -> Any:
        raise NotImplementedError

    def get_arp_table(self, ip=False) -> Any:
        raise NotImplementedError

    def get_interface_details(self, interface=False) -> Any:
        raise NotImplementedError

    def get_bfd_neighbors(self, interface=False) -> Any:
        raise NotImplementedError

    def get_ospf_neighbors(self, interface=False) -> Any:
        raise NotImplementedError

    def get_lldp_neighbors(self, interface=False) -> Any:
        raise NotImplementedError

    def get_transceiver_details(self, interface=False) -> Any:
        raise NotImplementedError
