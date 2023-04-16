"""
Vehicle and Traffic Light Network Interfacing Project
By: Joyce Fang and Nobu Shibata

There are three main entities in this application:
1. Traffic Light with three states:
    2 = Red
    1 = Yellow
    0 = Green
2. Car with Rank Number 1
3. Car with Rank Number 2

The purpose of this application is to limit the speed of each car (represented as a stepper motor)
depending on three parameters: the car object being controlled (contains the rank and the current speed), 
the current state of the traffic light.

With these three parameters, it's possible to control the speed at which the motor is running using
internetworking of things.

Hardware used:
1. Traffic Light - Zigbee Transmitter
2. Car 1 - 1 x Zigbee Transmitter, 1 x Zigbee Receiver
3. Car 2 - 1 x Zigbee Transmitter, 1 x Zigbee Receiver
"""

from car import Car
from traffic_light import TrafficLight

def main():
    # initialize the traffic light object
    traffic_light = TrafficLight("red")
    print(traffic_light)

    # initialize the car 1 object
    car1 = Car(1, 30)
    print(car1)

    # initialize the car 2 object
    car2 = Car(2, 30)
    print(car2)

if __name__ == "__main__":
    main()


# from digi.xbee.devices import XBeeDevice 
# import time  
# import random

# device_url = "/dev/cu.usbserial-00000000"  

# device = XBeeDevice(device_url, 9600) 
# device.open()  

# random.seed(777777)


# while True:     
    
#     trafficLightState = random.randint(0,3)
#     msg = input()      
#     device.send_data_broadcast(msg)     
#     try: 
#         device.send_data_broadcast(msg)     
#     except Exception as e:         
#         print(e, "No One Listening")     
#     print(msg)     
#     time.sleep(0.01)  
# device.close() 