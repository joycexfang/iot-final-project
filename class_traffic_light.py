"""
class_traffic_ligh.py is for the class TrafficLight. as TrafficLigh has multiple attributes
such as its state ("red", "yellow", "green") and its Zigbee device for transmitting messages
"""

from digi.xbee.devices import XBeeDevice
"""
Modify the device_url based on your port name
For Windows, go to Device Manage > Ports (typically COM7)
For Mac, do ‘ls /dev/cu.*’ in terminal (typically /dev/cu.usbserial-00000000)
For RPi, do ‘ls /dev/ttyUSB*’ in terminal (typically /dev/ttyUSB0)
"""

device_url = "/dev/cu.usbserial-00000000"

class TrafficLight:
    def __init__(self, initial_state):
        self.state = initial_state

        # Instantiate a local XBee node.
        self.device = XBeeDevice(device_url, 9600)
        self.device.open()
        

    def __str__(self):
        return "TRAFFIC LIGHT self.state: {}".format(self.state)
  
    def set_state(self, new_state):
        self.state = new_state

    # def change_state_from_current(self):
    #     # if the state of the light is red, change to green
    #     if self.state == "red":
    #         self.state = "green"
    #     # if the state of the light is green, change to yellow
    #     elif self.state == "green":
    #         self.state = "yellow"
    #     # otherwise (if the state of the light is yellow), change to red
    #     else:
    #         self.state = "red"

    #     print("changed self.state to:", self.state)

    def get_state(self):
        return self.state

    # this traffic light should only transmit messages to cars of rank 1
    def transmit_message(self, message, car_rank=1):
        self.device.send_data_broadcast(message)

    def close_zigbee(self):
        self.device.close()
