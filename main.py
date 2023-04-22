"""
Vehicle and Traffic Light Network Interfacing Project
By: Joyce Fang and Nobu Shibata

There are three main entities in this application:
1. Traffic Light with three states:
    2 = Red
    1 = Yellow
    0 = Green
2. Car with Rank Number = 1 (not starting from index 0 for ease of understandability)
3. Car with Rank Number = 2

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

from class_traffic_light import TrafficLight
import time

# This file is for the traffic light transmitter main program
def main():
    # create an instance of a traffic light object with an initial "red" light state,
    # a Zigbee Transmitter Device will also be instantiated here
    traffic_light = TrafficLight("red")

    try:
        # program for the traffic light transmitter using Zigbee device
        while True:
            message = input("Enter traffic light color (red, yellow, or green): ")
            
            print("Setting traffic light state:", message)
            traffic_light.set_state(message)

            print("Transmitting random traffic_light_state:", message)
            # traffic_light.transmit_message(message)
            try: 
                print("Will try transmitting random traffic_light_state:", message)
                # traffic_light.transmit_message(message)
            except Exception as e:
                print(e, "No car is listening.")
            
            print("You selected the color traffic light: ", message)
            time.sleep(0.01)

            print()
    
    except KeyboardInterrupt:
        print('Keyboard was interrupted!')
    
    print("Closing traffic light zigbee")
    # traffic_light.close_zigbee()

if __name__ == "__main__":
    main()
