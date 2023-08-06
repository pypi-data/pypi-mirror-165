# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
Function to query system's hard devices.
"""

import itertools
import sys
from typing import Dict

try:
    import pyudev
    pyudev.Context()
except ImportError:
    sys.exit("Unable to import package 'pyudev'. Please read the documentation")

from writer.config import IGNORED_DEVICE_PATHS
from writer.utils import get_readable_size


def query_disk_devices(readable=True) -> Dict[str, dict]:
    """
    Get information about all the available hard devices.
    """
    context = pyudev.Context()
    devs = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if any(_ in device.device_path for _ in IGNORED_DEVICE_PATHS):
            continue
        size = device.attributes.asint('size')
        if not size:
            continue
        if readable:
            readable_size = get_readable_size(size)
            dev = {'size': readable_size}
        else:
            dev = {'size': size * 512}
        for device_ in itertools.chain([device], device.ancestors):
            try:
                dev['model'] = device_.attributes.asstring('model').strip()
                break
            except KeyError:
                dev['model'] = ''
        devs[device.device_node] = dev
    return devs
