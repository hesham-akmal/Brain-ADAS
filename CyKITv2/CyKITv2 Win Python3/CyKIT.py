# -*- coding: utf-8 -*-
#
#  ♦ CyKIT ♦ 2018.May.24
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
#  CyKIT.py
#  Written by Warren
#
import os
import sys
import socket
import select
import struct
import eeg
import CyWebSocket
import threading
import time
import traceback
import inspect
#############################################################################################
from pynput import keyboard

def on_press(key):
    if(str(key) == 'Key.caps_lock'):

        cy_IO.onData(0,'CyKITv2:::RecordStart:::Subject')

def keyboardListener():
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def getCurrentPacket():
    return cy_IO.CurrentPacket
#########################################################################################
arg_count = len(sys.argv)

def mirror(custom_string):
        try:
            print(str(custom_string))
            return
        except OSError as exp:
            return

##################################################################################################################################################################
# Importing Airsim
# Uses local airsim package (DO NOT pip install, UNINSTALL IF INSTALLED ALREADY: "pip uninstall airsim")
from pathlib import Path
import sys
import os
import time
from ctypes import *
sys.path.append(str(Path().resolve().parent.parent).replace('\\','/') + '/AirSimClient')
sys.path.append(str(Path().resolve().parent.parent).replace('\\','/') + '/CarDetection/YOLO and Distance')
os.environ['PATH'] = str(Path().resolve().parent.parent).replace('\\','/') + '/AirSimClient' + os.pathsep + os.environ['PATH']
d = CDLL('SDL2.dll') #Steering kit haptic feedback dll
import BADAS_fns

BADAS_fns.SimConnectAndCheck()

RunVision_BADASbool = True

DriverBADAS = None
visionThread = None
if(RunVision_BADASbool):
    os.chdir("../../CarDetection/YOLO and Distance")
    import DriverBADAS
    visionThread = DriverBADAS.VisionThread(BADAS_fns)
    visionThread.start()
    os.chdir("../../CyKITv2/CyKITv2 Win Python3")

cy_IO = eeg.ControllerIO(BADAS_fns , visionThread , DriverBADAS)

def main(CyINIT):

    HOST = '127.0.0.1'
    PORT = 54123
    MODEL = 6
    check_connection = None

    #parameters = str(sys.argv[4]).lower()
    parameters = 'noweb'

    #  Stage 1.
    # ¯¯¯¯¯¯¯¯¯¯¯
    #  Acquire I/O Object.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    
    cy_IO.setInfo("ioObject", cy_IO)
    cy_IO.setInfo("config", parameters)

    if "verbose" in parameters: 
        cy_IO.setInfo("verbose","True")
    else:                   
        cy_IO.setInfo("verbose","False")

    if "noweb" in parameters:
        noweb = True
        cy_IO.setInfo("noweb","True")
        cy_IO.setInfo("status","True")
    else:
        noweb = False
        cy_IO.setInfo("noweb","False")
    
    if "noheader" in parameters:
        cy_IO.setInfo("noheader","True")

    if "openvibe" in parameters:
        cy_IO.setInfo("openvibe","True")


    headset = eeg.EEG(MODEL, cy_IO, parameters)
    
    while str(cy_IO.getInfo("DeviceObject")) == "0":
        time.sleep(.001)
        continue
    
    if "bluetooth" in parameters:
            mirror("> [Bluetooth] Pairing Device . . .")
    else:
        if "noweb" not in parameters:
            mirror("> Listening on " + HOST + " : " + str(PORT))

    mirror("> Trying Key Model #: " + str(MODEL))

    
    if "generic" in parameters:
        ioTHREAD = CyWebSocket.socketIO(PORT, 0, cy_IO)
    else:
        ioTHREAD = CyWebSocket.socketIO(PORT, 1, cy_IO)
    
    cy_IO.setServer(ioTHREAD)
    time.sleep(1)
    check_connection = ioTHREAD.Connect()
    ioTHREAD.start()
    
    while eval(cy_IO.getInfo("status")) != True:
        time.sleep(.001)
        continue   
    
    headset.start()
    
    CyINIT = 3

    ####################################################################################
    print("CONNECTED TO USB DONGLE")

    print("EPOC MODEL " + str(MODEL) + " needs to be ON")

    print("Caps Lock Toggles Recording EEG DATA")
    t = threading.Thread(target=keyboardListener)
    t.start() 
    ####################################################################################

    while CyINIT > 2:

        #print('while CyINIT > 2:')
        
        CyINIT += 1
        time.sleep(.001)
        
        if (CyINIT % 10) == 0:
            #print('if (CyINIT % 10) == 0:')
            
            check_threads = 0
            
            t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
            #if eval(cy_IO.getInfo("verbose")) == True:
            #    mirror(" Active Threads :{ " + str(t_array) + " } ")
            #time.sleep(15)
            
            if 'ioThread' in t_array:
                check_threads += 1
                
            if 'eegThread' in t_array:
                check_threads += 1
            
            #(1 if noweb == True else 2)

            if check_threads < (1 if noweb == True else 2):
                #print('if check_threads < (1 if noweb == True else 2):')
                
                threadMax = 2
                totalTries = 0
                while threadMax > 1 and totalTries < 2:
                    #print('while threadMax > 1 and totalTries < 2:')
                    totalTries += 1
                    time.sleep(0)
                    threadMax = 0

                    for t in threading.enumerate():
                        #print('for t in threading.enumerate():')
                        if "eegThread" in t.getName():
                            cy_IO.setInfo("status","False")
                            #mirror(t.getName())
                        if "ioThread" in t.getName():
                            #mirror(t.getName())
                            CyWebSocket.socketIO.stopThread(ioTHREAD)
                        
                        if "Thread-" in t.getName():
                            #mirror(t.getName())
                            threadMax += 1
                            try:
                                t.abort()
                            except:
                                continue
                t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
                #mirror(str(t_array))
                ioTHREAD.onClose("CyKIT.main() 1")
                mirror("*** Reseting . . .")
                CyINIT = 1
                main(1)

try:
    try:
        main(1)
    except OSError as exp:
        main(1)

except Exception as e:
    exc_type, ex, tb = sys.exc_info()
    imported_tb_info = traceback.extract_tb(tb)[-1]
    line_number = imported_tb_info[1]
    print_format = '{}: Exception in line: {}, message: {}'
    
    mirror("Error in file: " + str(tb.tb_frame.f_code.co_filename) + " >>> ")
    mirror("CyKITv2.Main() : " + print_format.format(exc_type.__name__, line_number, ex))
    mirror(traceback.format_exc())
    
    mirror(" ) WARNING_) CyKIT2.main E1: " + str(e))
    mirror("Error # " + str(list(OSError)))
    mirror("> Device Time Out or Disconnect . . .  [ Reconnect to Server. ]")
    main(1)