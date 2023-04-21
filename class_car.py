import math # import math library
import time # import the time module
from digi.xbee.devices import XBeeDevice

"""
Modify the device_url based on your port name
For Windows, go to Device Manage > Ports (typically COM7)
For Mac, do ‘ls /dev/cu.*’ in terminal (typically /dev/cu.usbserial-00000000)
For RPi, do ‘ls /dev/ttyUSB*’ in terminal (typically /dev/ttyUSB0)
"""

device_url = "/dev/cu.usbserial-00000000"

tracking = time.time()

class Car:
    def __init__(self, rank, max_speed):
        self.rank = rank
        self.max_speed = max_speed
        self.curr_speed = 0

        # Instantiate a local XBee node.
        self.device = XBeeDevice(device_url, 9600)
        self.device.open()

    def __str__(self):
        return "CAR self.rank: {} \t self.max_speed: {} \t self.curr_speed: {}".format(self.rank, self.max_speed, self.curr_speed)

    def change_speed(self):
        # in one whole second, there will be number of "refreshes" to either limit the speed or increase the speed
        self.refresh_speed()
        # print("changed self.curr_speed to:", self.curr_speed)

    def calculate_speed(self, light_color):
        return self.curr_speed - (light_color) * (1 - (1/math.pow(math.e, 1.5*self.rank))) * 1.2

    def refresh_speed(self):
        oldtime = time.time()
        break_loop = False
        while not break_loop:
            if self.second_passed(oldtime):
                print("1 second passed")
                break_loop = True
                break
            time.sleep(0.25)
            print("0.25 seconds passed")

    def second_passed(self, oldepoch):
        return time.time() - oldepoch >= 1

    # only car of rank 1 should transmit messages to car of rank 2
    def transmit_message(self, message):
        if self.rank != "1":
            return "cannot transmit message from a non-rank 1 car"
        else:
            self.device.send_data_broadcast(message)

    
    # car of rank 1 can only receive from traffic light
    # car of rank 2 can only receive from car of rank 1
    def receive_message(self):
        return self.device.read_data()

    def close_zigbee(self):
        self.device.close()
