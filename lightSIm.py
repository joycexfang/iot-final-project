# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:43:15 2023

@author: andre
Traffic Light 

2 = Red
1 = Yellow
0 = Green
"""
from digi.xbee.devices import XBeeDevice 
import time  
import random

device_url = "/dev/cu.usbserial-00000000"  

device = XBeeDevice(device_url, 9600) 
device.open()  

random.seed(777777)


while True:     
    
    trafficLightState = random.randint(0,3)
    msg = input()      
    device.send_data_broadcast(msg)     
    try: 
        device.send_data_broadcast(msg)     
    except Exception as e:         
        print(e, "No One Listening")     
    print(msg)     
    time.sleep(0.01)  
device.close() 