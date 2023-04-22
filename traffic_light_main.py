"""
traffic_light_main.py is the main program used to transmit messages from the 
traffic light to another device on the network (i.e. car of rank 1)
pi@192
"""
from class_traffic_light import TrafficLight
import time
import RPi.GPIO as GPIO


# This file is for the traffic light transmitter main program
def main():
    # create an instance of a traffic light object with an initial "red" light state,
    # a Zigbee Transmitter Device will also be instantiated here
    traffic_light = TrafficLight("red")
    
    """
    try:
        # program for the traffic light transmitter using Zigbee device
        while True:
            message = input("Enter traffic light color (red, yellow, or green): ")
            
            print("Setting traffic light state:", message)
            traffic_light.set_state(message)
            try: 
                print("Transmitting traffic_light_state:", message)
                traffic_light.transmit_message(message)
            except Exception as e:
                print(e, "No car is listening.")
            
            print("You selected the color traffic light: ", message)
            time.sleep(0.01)

            print()
    
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting program...')
    """

    grn = 13
    yel = 15
    red = 18
    # Set up GPIO mode and pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(grn, GPIO.OUT)  # Red LED on GPIO 18
    GPIO.setup(yel, GPIO.OUT)  # Green LED on GPIO 23
    GPIO.setup(red, GPIO.OUT)  # Blue LED on GPIO 24

    while(1):

        # Turn on green for 10 sec
        GPIO.output(grn, GPIO.HIGH)
        traffic_light.set_state("green")
        traffic_light.transmit_message(traffic_light.get_state(), car_rank=1)
        time.sleep(10)
        GPIO.output(grn, GPIO.LOW)
        time.sleep(0.1)

        #Turn on yellow for 2 sec
        GPIO.output(yel, GPIO.HIGH)
        traffic_light.set_state("yellow")
        traffic_light.transmit_message(traffic_light.get_state(), car_rank=1)
        time.sleep(2)
        GPIO.output(yel, GPIO.LOW)
        time.sleep(0.1)

        #Turn on red for 10 sec
        GPIO.output(red, GPIO.HIGH)
        traffic_light.set_state("red")
        traffic_light.transmit_message(traffic_light.get_state(), car_rank=1)
        time.sleep(10)
        GPIO.output(red, GPIO.LOW)
        time.sleep(0.1)

    # Clean up GPIO pins
        GPIO.cleanup()
        print("Closing traffic light zigbee")
        traffic_light.close_zigbee()

if __name__ == "__main__":
    main()
