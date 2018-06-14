#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json

from xcathwctl import OpenBMCManager

def loadData(file_name):

    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':

    data = loadData('data.json')
    manager = OpenBMCManager(data, json_fmt=False, debug=False, verbose=True)
    result = manager.power_bmc_state()
    print result
