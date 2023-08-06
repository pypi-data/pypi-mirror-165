# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umnet_pyncs', 'umnet_pyncs.state', 'umnet_pyncs.state.models']

package_data = \
{'': ['*']}

install_requires = \
['multiprocessing-logging>=0.3.3,<0.4.0', 'ntc-templates>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'umnet-pyncs',
    'version': '0.1.3',
    'description': 'custom python module for NCS helpers',
    'long_description': '## Overview\n\nThis module is intended to be installed on the production NCS nodes and imported in other services/actions that need to gather state from the network.  It uses the NCS device manager and the standard python `multiprocessing` library to connect to devices in-parallel and issue commands, returning results as structured data.\n\n## Usage information\n\nBasic usage example in an NCS callback:\n\n``` python\nfrom umnet_ncs.state import StateManager\n...\n\n\nclass DemoAction(Action):\n    @Action.action\n    def cb_action(self, uinfo, name, kp, input, output, trans):\n        ...\n        with StateManager() as m:\n            interfaces = m.get_state(al_devices, ["get-interface-details"])\n            arp = m.get_state(dl_devices, ["get-arp-table"])\n            ...\n```\n\n## Supported commands\n\nWe attempt to normalize the output of each command based on how it is implemented.  For example, we might default to just directly returning the data as-parsed by the `ntc_templates` module, or try and emulate for e.g. junos devices where we might have direct access to NETCONF RPCs via the NCS device manager.\n\nCurrently supported commands are:\n- `get-mac-table`\n- `get-arp-table`\n- `get-interface-details`\n- `get-transciever-details`\n\n## TODO\nThe models are mostly taken verbatim from the `netsplash` NCS package, and additional methods were added on top to support the [stats.py](https://gitlab.umich.edu/its-inf-net/umnet-ncs-dev/-/blob/master/packages/umnet-backbone/python/fabric/stats.py) module.\n',
    'author': 'Nick Grundler',
    'author_email': 'grundler@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
