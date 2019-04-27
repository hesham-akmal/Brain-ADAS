#!/usr/bin/python
# -*- coding: utf-8 -*-

# Use local airsim package (DO NOT pip install airsim, UNINSTALL IF ALREADY INSTALLED > "pip uninstall airsim")
import numpy as np
import math

# To view images
from PIL import Image
import io

# To estimate code time, gets timestamp
import time

#gets timestamp
import datetime

# To play sounds
import winsound

import threading
import sys

import airsim

################################################################################################################################################################################
################################################################################################################################################################################

#client = airsim.CarClient()

def Find_BADAS_ClientNormal():
    global client
    client = airsim.CarClient()

def Find_BADAS_Client(): #Thread
    threading.Thread(target=Find_BADAS_ClientNormal).start()

#Feedback Haptic effects
import sdl2 #Local sdl2 dir which is a wrapper to SDL2.dll

class Haptic:

    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_TIMER | sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_HAPTIC)

        #print("Trying to find haptics")
        if (sdl2.SDL_NumHaptics() == 0):
            print("No haptic devices found, Driving kit not connected.")
            sdl2.SDL_Quit()

        for index in range(0, sdl2.SDL_NumHaptics()):
            print("Found", index, ":", sdl2.SDL_HapticName(index))
        index = 0

        self.haptic = sdl2.SDL_HapticOpen(index)
        if self.haptic == None:
            print("Unable to open device")
            sdl2.SDL_Quit()
            exit(0)
        else:
            #print("Using device", index)
            pass

        self.nefx = 0
        self.efx = [0] * 12
        self.id = [0] * 12
        supported = sdl2.SDL_HapticQuery(self.haptic)
    
        if (supported & sdl2.SDL_HAPTIC_SINE):
            print("   effect", self.nefx, "Sine Wave")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SINE, periodic= \
                sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(9000,0,0)), \
                period=1000, magnitude=0x4000, length=5000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1

        if (supported & sdl2.SDL_HAPTIC_TRIANGLE):
            print("   effect", self.nefx, "Triangle")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_TRIANGLE, periodic= \
                sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_CARTESIAN, dir=(1,0,0)), \
                period=1000, magnitude=0x4000, length=5000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1

        if (supported & sdl2.SDL_HAPTIC_SAWTOOTHUP):
            print("   effect", self.nefx, "Sawtooth Up")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SAWTOOTHUP, periodic= \
                sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SAWTOOTHUP, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(9000,0,0)), \
                period=500, magnitude=0x5000, length=5000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1

        if (supported & sdl2.SDL_HAPTIC_SAWTOOTHDOWN):
            print("   effect", self.nefx, "Sawtooth Down")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SAWTOOTHDOWN, periodic= \
                sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SAWTOOTHDOWN, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_CARTESIAN, dir=(1,0,0)), \
                period=500, magnitude=0x5000, length=5000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1

        if (supported & sdl2.SDL_HAPTIC_RAMP):
            print("   effect", self.nefx, "Ramp")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_RAMP, ramp= \
                sdl2.SDL_HapticRamp(type=sdl2.SDL_HAPTIC_RAMP, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(9000,0,0)), \
                start=0x5000, end=0x0000, length=5000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1

        if (supported & sdl2.SDL_HAPTIC_CONSTANT):
            print("   effect", self.nefx, "Constant Force")
            self.efx[self.nefx] = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_CONSTANT, constant= \
                sdl2.SDL_HapticConstant(type=sdl2.SDL_HAPTIC_CONSTANT, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_CARTESIAN, dir=(1,0,0)), \
                length=5000, level=0x4000, attack_length=1000, fade_length=1000))
            self.id[self.nefx] = sdl2.SDL_HapticNewEffect(self.haptic, self.efx[self.nefx])
            self.nefx += 1
    
    def start_haptic(self,haptic_number):
        sdl2.SDL_HapticRunEffect(self.haptic, self.id[haptic_number], 1)

    def stop_haptic(self):
        sdl2.SDL_HapticStopAll(self.haptic)

import time
h = Haptic()

def BeepAlertStart():
    for i in range(2):
        winsound.Beep(500, 100)
        
def StartFullBrake():
    client.setBrakeInput(1)
    threading.Thread(target=BeepAlertStart).start()

def StopBrake():
    client.setBrakeInput(0)
        
# Overrides brake control and brakes until speed is less than 1        
def EmergencyBrake_TillCarStop():
    h.start_haptic(5) # Start Steering wheel Haptic
    StartFullBrake()
    
#     Keep brakes on till car speed almost zero
    while(client.getCarState().speed > 1):
        time.sleep(0.1)
    
    StopBrake()
    h.stop_haptic()