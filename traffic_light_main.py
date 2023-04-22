"""
traffic_light_main.py is the main program used to transmit messages from the 
traffic light to another device on the network (i.e. car of rank 1)
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

            print("Transmitting traffic_light_state:", message)
            traffic_light.transmit_message(message)
            try: 
                print("Will try transmitting traffic_light_state:", message)
                traffic_light.transmit_message(message)
            except Exception as e:
                print(e, "No car is listening.")
            
            print("You selected the color traffic light: ", message)
            time.sleep(0.01)

            print()
    
    except KeyboardInterrupt:
        print('Keyboard was interrupted!')
    
    print("Closing traffic light zigbee")
    traffic_light.close_zigbee()

if __name__ == "__main__":
    main()
