#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# CyKIT v2 - 2017.12.23
# =======================
# Written by Warren
# Modified by tahesse

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import threading

import CyWebSocket
import eeg

arg_count = len(sys.argv)

if arg_count == 1 or arg_count > 5 or sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[
    1] == "/?":
    print(
        '''\r\n
        (Version: CyKITv2:2017.12.15) -- Python 2.7.6 on Win32
        \r\n Usage: python CyKITv2.py <IP> <Port> <Model#(1-6)> [config] \r\n
        {hline}\r\n
        <IP> <PORT> for CyKIT to listen on. \r\n
        {hline}\r\n
        <Model#> Choose the decryption type. \r\n
               1 - Epoc (Research)\r\n
               2 - Epoc (Standard)\r\n
               3 - Insight (Research)\r\n
               4 - Insight (Standard)\r\n
               5 - Epoc+ (Research)\r\n
               6 - Epoc+ (Standard)\r\n\r\n
        {hline}\r\n
        [config] is optional. \r\n
         'info' prints additional information into console.\r\n
         'confirm'  Requests you to confirm a device everytime device is initialized.\r\n
         'nocounter'  Removes all counters from 'all' outputs.\r\n
         'format-0' (Default) Outputs 14 data channels in float format. ('4201.02564096') \r\n
         'format-1' Outputs the raw data (to be converted by Javascript or other). \r\n
         'outputdata'  Prints the (formatted) data being sent, to the console window.\r\n
         'outputencrypt'  Prints the (encrypted) rjindael data to the console window.\r\n\r\n
          Join these words together, using a + separator. \r\n
          (e.g  info+confirm ) \r\n\r\n
        {hline}\r\n
         Example Usage: \r\n
         python CyKITv2.py 127.0.0.1 55555 1 info+confirm \r\n\r\n
        {hline}
        '''.format(hline='_' * 85))
    sys.argv = [sys.argv[0], "127.0.0.1", "55555", "1", ""]

if arg_count < 5:

    if arg_count == 2:
        sys.argv = [sys.argv[0], sys.argv[1], "55555", "1", ""]
    if arg_count == 3:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "1", ""]
    if arg_count == 4:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], ""]

"""
TODO
 
  Settings Buttons
   . Change Epoc+ settings mode.
  
  Send openvibe stream (using cyos template)
  
  Add Tabs
  
  Create CSS
   
  Associate checkboxes with drawing data.
  
"""


def main(CyINIT):
    # obtain global CyINIT
    CyINIT = locals().get('CyINIT', 2)

    CyINIT += 1
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    MODEL = int(sys.argv[3])

    # Initialize CyKIT 
    if CyINIT == 2:
        global ioTHREAD  # FIXME

        print('> Listening on {host}:{port}'.format(host=HOST, port=PORT))
        print("> Probing Key Model #: {model}".format(model=MODEL))

        myi = eeg.MyIO()
        ioTHREAD = CyWebSocket.socketIO(PORT, 1, myi)
        myi.setServer(ioTHREAD)
        check_connection = ioTHREAD.Connect()
        cyIO = ioTHREAD.start()
        cyHeadset = eeg.EEG(MODEL, myi, str(sys.argv[4])).start()
        for t in threading.enumerate():
            print(str(t.getName()))
        CyINIT += 1

    # Loop.

    while CyINIT > 2:
        CyINIT += 1

        if CyINIT > 100:
            modelCheck = myi.modelChange()  # FIXME
            if modelCheck != 0:
                MODEL = modelCheck

            CyINIT = 3
            check_threads = 0
            for t in threading.enumerate():
                if t.getName() == "ioThread" or t.getName() == "eegThread":
                    check_threads += 1

            if check_threads == 1:
                ioTHREAD.onClose()
                print("*** Reseting . . .")
                CyINIT = 1
                main(1)


if __name__ == '__main__':
    try:
        main(1)
    except Exception as e:
        print(e)
        print("Device Time Out or Disconnect . . .    Reconnect to Server.")
        main(1)
