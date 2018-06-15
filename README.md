# xcathwctl

## Installation

``python setup.py install``

## Import xcathwctl

``import xcathwctl``

## Instantiation

``OpenBMCManager(data, json_fmt=False, debug=False, verbose=True)``

``node_dict`` is a dict contains node, bmcip, bmc, username, password. Format as: ``{"node1": {"bmcip": "x.x.x.x", "username": "root", "password": "xxxxxx"}, "node2": {"bmcip": "x.x.x.x", "username": "root", "password": "xxxxxx"}}``

``verbose`` is bool, if "True" will print out verbose information.

## Methods of OpenBMCManager:

``def inventory``: show all inventory information

``def inv_cpu``: show CPU information

``def dimm``: show DIMM information

``def firm``: show firmware information

``def power_state``: show host power status

``def power_on``: power on host

``def power_off``: power off host

``def power_softoff``: power softoff host

``def power_reset``: reset host

``def power_boot``: boot host

``def power_bmc_state``: show bmc status

``def power_bmc_reboot``: reboot bmc

## Return data from OpenBMCManager:

Json or dict. If set ``json_fmt`` as "True", return json format result. If "False", return dict fromat. Default is "json".

This is json format:

``{"node1": {"data": ["BMC Ready"], "rc": 0}, "node2": {"data": ["BMC Ready"], "rc": 0}}``

## Example

```
from xcathwctl import OpenBMCManager
manager = OpenBMCManager(node_dict, verbose)
result = manager.power_state()
```

**example.py** is an example file to call method of xcathwctl to run rpower command.
