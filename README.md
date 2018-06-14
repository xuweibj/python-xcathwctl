# xcathwctl

## Installation

``python setup.py install``

## Import xcathwctl

``import xcathwctl``

## Instantiation

``OpenBMCManager(node_dict, debug, verbose)``

``node_dict`` is a dict contains node, bmcip, bmc, username, password. Format as: ``{"node1": {"bmcip": "x.x.x.x", "username": "root", "password": "xxxxxx"}, "node2": {"bmcip": "x.x.x.x", "username": "root", "password": "xxxxxx"}}``

``verbose`` is bool, if "True" will print out verbose information.

## Methods of OpenBMCManager:

``def power_state``      : show host power status

``def power_on``         : power on host

``def power_off``        : power off host

``def power_softoff``    : power softoff host

``def power_reset``      : reset host

``def power_boot``       : boot host

``def power_bmc_state``  : show bmc status

``def power_bmc_reboot`` : reboot bmc

## Return data from openbmc_manager:

json type as below:

``{"node1": {"data": ["BMC Ready"], "rc": 0}, "node2": {"data": ["BMC Ready"], "rc": 0}}``

## Example

```
from xcathwctl import OpenBMCManager
manager = OpenBMCManager(node_dict, verbose)
result = manager.power_state()
```

**example.py** is an example file to call method of xcathwctl to run rpower command.
