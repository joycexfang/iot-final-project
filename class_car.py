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

step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

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

        self.GPIO_init()
        self.motor_pins = [in1,in2,in3,in4]
        self.motor_step_counter = 0
        
        # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
        self.step_sleep = 0.001

    def __str__(self):
        return "CAR self.rank: {} \t self.max_speed: {} \t self.curr_speed: {}".format(self.rank, self.max_speed, self.curr_speed)

    def GPIO_init(self):
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
    
    def cleanup(self):
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )
        GPIO.cleanup()

    def spin_up(self):
        # the meat
        try:
            i = 0
            for i in range(step_count):
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output( self.motor_pins[pin], step_sequence[self.motor_step_counter][pin] )
                if direction==True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                elif direction==False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    self.cleanup()
                    exit( 1 )
                time.sleep( self.step_sleep )
        except KeyboardInterrupt:
            self.cleanup()
            exit( 1 )

        self.cleanup()
        exit( 0 )

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
