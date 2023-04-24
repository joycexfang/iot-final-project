"""
class_car.py is for the class Car. as Car has multiple attributes such as rank,
max speed, curr speed, zigbee device/(s), motor pins, motor step counter, and step sleep

the Car class can calculate and control the speed of the car AND it can receive and
transmit messages from/to other devices on the network
"""

import math # import math library
import time # import the time module
from digi.xbee.devices import XBeeDevice
#This code was taken from https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/
#!/usr/bin/python3
import RPi.GPIO as GPIO

in1 = 17
in2 = 18
in3 = 27
in4 = 22

"""
Modify the device_url based on your port name
For Windows, go to Device Manage > Ports (typically COM7)
For Mac, do ‘ls /dev/cu.*’ in terminal (typically /dev/cu.usbserial-00000000)
For RPi, do ‘ls /dev/ttyUSB*’ in terminal (typically /dev/ttyUSB0)
"""
device_url_receiver = "/dev/ttyUSB0"
device_url_transmitter = "/dev/ttyUSB1"
tracking = time.time()

class Car:
    def __init__(self, position_rank, max_speed):
        self.position_rank = position_rank
        self.max_speed = max_speed
        self.curr_speed = 0

        # Instantiate a local XBee node FOR RECEIVER.
        self.device_receiver = XBeeDevice(device_url_receiver, 9600)
        self.device_receiver.open()

        # car of rank 1 also has a transmitter Zigbee device
        if self.position_rank == 1:
            # Instantiate a local XBee node FOR TRANSMITTER.
            self.device_transmitter = XBeeDevice(device_url_transmitter, 9600)
            self.device_transmitter.open()

        self.initialize_motor_pins()
        self.motor_pins = [in1,in2,in3,in4]
        self.motor_step_counter = 0

        # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
        self.step_sleep = 0.001

        # self.need_transmit = False
        self.msg_data = "green"

    def __str__(self):
        return "CAR self.position_rank: {} \t self.max_speed: {} \t self.curr_speed: {}".format(self.position_rank, self.max_speed, self.curr_speed)

    def initialize_motor_pins(self):
        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( in1, GPIO.OUT )
        GPIO.setup( in2, GPIO.OUT )
        GPIO.setup( in3, GPIO.OUT )
        GPIO.setup( in4, GPIO.OUT )

        # initializing
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )

    def clean_up_motor_pins(self):
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )
        GPIO.cleanup()

    def adjust_speed(self):
    #     # in one whole second, there will be number of "refreshes" to either limit the speed or increase the speed
    #     # print("changed self.curr_speed to:", self.curr_speed)

        light_state = self.msg_data
        print("---------------");
        print(light_state)
        print("---------------");
        if(light_state == "green"):

            self.step_sleep = 0.001
        elif(light_state == "yellow"):
            self.step_sleep += 0.5*((1-(1/(math.exp(1.5*(self.position_rank/2)))))/65)
        elif(light_state == "red"):
            self.step_sleep += ((1-(1/(math.exp(1.5*(self.position_rank/2)))))/65)

    # def calculate_speed(self, light_color):
    #     return self.curr_speed - (light_color) * (1 - (1/math.pow(math.e, 1.5*self.position_rank))) * 1.2

    # only car of rank 1 should transmit messages to car of rank 2
    def transmit_message(self, message):
        self.device_transmitter.send_data_broadcast(message)
        # self.need_transmit = False

    # car of rank 1 can only receive from traffic light
    # car of rank 2 can only receive from car of rank 1
    def receive_message(self):
        # self.need_transmit = True
        return self.device_receiver.read_data()

    def set_msg_data(self, msg):
        self.msg_data = msg

    # def get_need_transmit(self):
    #     return self.need_transmit

    def get_msg_data(self):
        return self.msg_data

    def close_zigbee_receiver(self):
        self.device_receiver.close()

    def close_zigbee_transmitter(self):
        self.device_transmitter.close()
