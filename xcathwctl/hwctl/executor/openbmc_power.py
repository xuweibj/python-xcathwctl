#!/usr/bin/env python
###############################################################################
# IBM(c) 2018 EPL license http://www.eclipse.org/legal/epl-v10.html
###############################################################################
# -*- coding: utf-8 -*-
#
from __future__ import print_function
import gevent
import time

from xcathwctl.common.task import ParallelNodesCommand
from xcathwctl.common.exceptions import SelfClientException, SelfServerException
from xcathwctl.hwctl import openbmc_client as openbmc

import logging
logger = logging.getLogger('xcathwctl')


POWER_STATE_DB = {
    "on"      : "powering-on",
    "off"     : "powering-off",
    "softoff" : "powering-off",
    "boot"    : "powering-on",
    "reset"   : "powering-on",
}
class OpenBMCPowerTask(ParallelNodesCommand):
    """Executor for power-related actions."""

    power_result = {}

    def get_state(self, **kw):

        node = kw['node']
        obmc = openbmc.OpenBMCRest(name=node, nodeinfo=kw['nodeinfo'], messager=self.callback,
                                   debugmode=self.debugmode, verbose=self.verbose)
        state = 'Unknown'
        try:
            obmc.login()
            states = obmc.list_power_states()
            state = obmc.get_host_state(states)
            result = openbmc.RPOWER_STATES.get(state, state)
            self.callback.info('%s: %s' % (node, result))
            self.power_result.update({node: {'rc': 0, 'data': [result]}})

        except (SelfServerException, SelfClientException) as e:
            self.callback.error(e.message, node)
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}}) 

        return state

    def get_bmcstate(self, **kw):

        node = kw['node']
        obmc = openbmc.OpenBMCRest(name=node, nodeinfo=kw['nodeinfo'], messager=self.callback,
                                   debugmode=self.debugmode, verbose=self.verbose)
        bmc_not_ready = bmc_state = 'NotReady'
        try:
            obmc.login()
        except (SelfServerException, SelfClientException) as e:
            self.callback.error(e.message, node)
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}})
            return bmc_state

        try:
            state = obmc.get_bmc_state()
            bmc_state = state.get('bmc')

            if bmc_state != 'Ready':
                bmc_state = bmc_not_ready

            result = openbmc.RPOWER_STATES.get(bmc_state, bmc_state)
            self.callback.info('%s: %s' % (node, result))
            self.power_result.update({node: {'rc': 0, 'data': [result]}})

        except SelfServerException as e:
            result = openbmc.RPOWER_STATES[bmc_not_ready]
            self.callback.error(result, node)
            self.power_result.update({node: {'rc': 1, 'data': [result]}})
        except SelfClientException as e:
            result = "%s (%s)" % (openbmc.RPOWER_STATES[bmc_not_ready], e.message)
            self.callback.error(result, node)
            self.power_result.update({node: {'rc': 1, 'data': [result]}})

        return bmc_state

    def set_state(self, state, **kw):

        node = kw['node']
        obmc = openbmc.OpenBMCRest(name=node, nodeinfo=kw['nodeinfo'], messager=self.callback,
                                   debugmode=self.debugmode, verbose=self.verbose)
        try:
            obmc.login()
            ret = obmc.set_power_state(state)
            new_status = POWER_STATE_DB.get(state, '')

            self.callback.info('%s: %s' % (node, state))
            self.power_result.update({node: {'rc': 0, 'data': [state]}})
            if new_status:
                self.callback.update_node_attributes('status', node, new_status)
        except (SelfServerException, SelfClientException) as e:
            self.callback.error(e.message, node)
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}})

    def reboot(self, optype='boot', **kw):

        node = kw['node']
        obmc = openbmc.OpenBMCRest(name=node, nodeinfo=kw['nodeinfo'], messager=self.callback,
                                   debugmode=self.debugmode, verbose=self.verbose)
        try:
            obmc.login()
            states = obmc.list_power_states()
            status = obmc.get_host_state(states)

            new_status =''
            if optype == 'reset' and status in ['Off', 'chassison']:
                status = openbmc.RPOWER_STATES['Off']
                self.callback.info('%s: %s'  % (node, status))
                self.power_result.update({node: {'rc': 0, 'data': [status]}})
            else:
                if status not in ['Off', 'off']:
                    obmc.set_power_state('off')
                    self.callback.update_node_attributes('status', node, POWER_STATE_DB['off'])

                    off_flag = False
                    start_timeStamp = int(time.time())
                    for i in range (0, 30):
                        states = obmc.list_power_states()
                        status = obmc.get_host_state(states)
                        if openbmc.RPOWER_STATES.get(status) == 'off':
                            off_flag = True
                            break
                        gevent.sleep( 2 )

                    end_timeStamp = int(time.time())

                    if not off_flag:
                        error = 'Error: Sent power-off command but state did not change ' \
                                 'to off after waiting %s seconds. (State= %s).' % (end_timeStamp - start_timeStamp, status)
                        self.power_result.update({node: {'rc': 1, 'data': [error]}})
                        return self.callback.error(error, node) 

                ret = obmc.set_power_state('on')
                self.callback.update_node_attributes('status', node, POWER_STATE_DB['on'])

                self.callback.info('%s: %s'  % (node, 'reset'))
                self.power_result.update({node: {'rc': 0, 'data': ['reset']}})

        except (SelfServerException, SelfClientException) as e:
            self.callback.error(e.message, node)
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}})

    def reboot_bmc(self, optype='warm', **kw):

        node = kw['node']
        obmc = openbmc.OpenBMCRest(name=node, nodeinfo=kw['nodeinfo'], messager=self.callback,
                                   debugmode=self.debugmode, verbose=self.verbose)
        new_status = ''
        try:
            obmc.login()
        except (SelfServerException, SelfClientException) as e:
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}})
            return self.callback.error(e.message, node)

        firm_obj_dict = {}
        try:
            has_functional, firm_obj_dict = obmc.list_firmware()
        except (SelfServerException, SelfClientException) as e:
            self.callback.syslog('%s: %s' % (node, e.message))

        clear_flag = False
        for key, value in firm_obj_dict.items():
            if not value.functional and value.priority == 0:
                clear_flag = True
                break

        if clear_flag:
            self.callback.info('%s: Firmware will be flashed on reboot, deleting all BMC diagnostics...' % node)
            try:
                obmc.clear_dump('all')
            except (SelfServerException, SelfClientException) as e:
                self.callback.warn('%s: Could not clear BMC diagnostics successfully %s' % (node, e.message))

        try:
            obmc.reboot_bmc(optype)
        except (SelfServerException, SelfClientException) as e:
            self.power_result.update({node: {'rc': 1, 'data': [e.message]}})
            self.callback.error(e.message, node)
        else:
            result = openbmc.RPOWER_STATES['bmcreboot']
            self.power_result.update({node: {'rc': 0, 'data': [result]}})
            self.callback.info('%s: %s' % (node, result))

    def result(self):

        return self.power_result

