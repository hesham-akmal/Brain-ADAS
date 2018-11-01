# -*- coding: utf8 -*-
#
# CyKIT v2 - 2018.Jan.29
# ========================
# Written by Warren
#

import sys
import socket
import select
import struct
import eeg
import CyWebSocket
import threading
import time

import time , os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def headset_data_recorder(file_name , session_timeout):
    path = os.getcwd() + '\CyKITv2.html'
    driver = webdriver.Chrome()

    try:
        #Parse the html file
        soup = BeautifulSoup(open(path) , 'html5lib')
        driver.get('file://' + path)
        
        #Click on Connect button then wait 5 secs
        driver.find_element_by_xpath('//*[@id="cyConnect"]').click()
        
        #Click on Recording tab
        driver.find_element_by_xpath('/html/body/div[4]/button[4]').click()
        
        #Change the output file's name
        driver.find_element_by_xpath('//*[@id="cyRecordFile"]').click()
        driver.find_element_by_xpath('//*[@id="cyRecordFile"]').clear()
        driver.find_element_by_xpath('//*[@id="cyRecordFile"]').send_keys(file_name)
        
        #Click on Record button
        driver.find_element_by_xpath('//*[@id="cyStartRecord"]').click()
        
        #Wait for the session to end then click on Stop button
        time.sleep(session_timeout)
        driver.find_element_by_xpath('//*[@id="cyStopRecord"]').click()
        
        #Exit
        driver.close()
        os._exit(1)

    except NoSuchElementException as e:
        print(e)

    
   
def main(CyINIT):

    if 'CyINIT' not in locals():
        #global CyINIT
        CyINIT = 2
   
    CyINIT += 1
    HOST = '127.0.0.1'
    PORT = 55555
    MODEL = 6
    
    # Initialize CyKIT 
    if CyINIT == 2:
        global ioTHREAD
        print "> Listening on " + HOST + " : " + str(PORT)
        print "> Trying Key Model #: " + str(MODEL)
        
        myi = eeg.MyIO()

        #webbrowser.open('CyKITv2.html')
        #N = input('How many subjects do you want to run the script for? ')
        #for i in range(int(N)):
            # file_name = input('Output file name? ')
            # session_timeout = input('Session period in minutes: ')
            #headset_data_recorder('jhvjv' , int(session_timeout)*60)


        t = threading.Thread(target = headset_data_recorder, args = ('subject' , 10))
        t.start()

        ioTHREAD = CyWebSocket.socketIO(PORT, 1, myi)
        myi.setServer(ioTHREAD)
        check_connection = ioTHREAD.Connect()
        cyIO = ioTHREAD.start()
        
        cyHeadset = eeg.EEG(MODEL, myi, '').start()
        
        for t in threading.enumerate():
            print str(t.getName())
        CyINIT += 1

    while CyINIT > 2:
        CyINIT += 1
        
        if CyINIT > 1000:
            modelCheck = myi.modelChange()
            if modelCheck != 0:
                MODEL = modelCheck
            
            CyINIT = 3
            check_threads = 0
            #print "testing"
            
            for t in threading.enumerate():
                if t.getName() == "ioThread" or t.getName() == "eegThread":
                    check_threads += 1
            if check_threads == 1:
                ioTHREAD.onClose()
                print "*** Reseting . . ."
                CyINIT = 1
                main(1)
    
try:
    
    main(1)
  
except Exception, e:
    print e
    print "Device Time Out or Disconnect . . .    Reconnect to Server."
    main(1)
