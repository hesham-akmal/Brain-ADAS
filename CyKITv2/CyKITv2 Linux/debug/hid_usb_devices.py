#!/usr/bin/env python

"""Debug hidapi python library and hid devices.

You may use this utility script for debugging purposes to check if this library does work as
intended, thus detecting all plugged hid devices.

This files does also provide you with the vendor_id and product_id required by the udev rule.
"""

import hidapi

hidapi.hid_init()

for dev in hidapi.hid_enumerate():
    print(50 * '-')
    print(dev.description())
