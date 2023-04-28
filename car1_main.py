"""
car1_main.py is the main program used to receive and transmit messages from other
devices on the network. it will run three process concurrently (receiver, transmitter, and motor controller)

the flow of communication goes like so:
traffic light transmits message -> car 1 receives message
car 1 transmits message -> car 2 receives message
"""

import threading
import time
from class_car import Car
import RPi.GPIO as GPIO

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

car_object = Car(1,30)

# main thread for car 1 receiver
def receiver():
    # program for the car 1 receiver using Zigbee device
    while True:
        # Receive data
        try:
            global car_object
            xbee_message = car_object.receive_message()
            if xbee_message:
                data = xbee_message.data

                # setting msg data so that transmit can occur
                car_object.set_msg_data(data.decode('UTF-8'))
                sender = xbee_message.remote_device
                timestamp = xbee_message.timestamp
                msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender, data=data.decode('UTF8'))
                print(msg)

                car_object.transmit_message(data.decode('UTF-8'))
                try:
                    print("CAR1_TRANSMITTER: Attempting to transmit message from car 1 to car 2:", data.decode('UTF-8'))
                    car_object.transmit_message(data.decode('UTF-8'))
                except Exception as e:
                    print(e, "CAR1_TRANSMITTER: No car is listening.")
                print()
        except Exception as e:
            print(e, "Error occurred while receiving message.")

# main thread for car 1 motor controller
def motor_controller():
    while True:
        # Control a motor or other actuator
        print("CAR1_MOTOR: Controlling motor...")

        # the meat
        i = 0
        for i in range(step_count):
            global car_object
            for pin in range(0, len(car_object.motor_pins)):
                GPIO.output( car_object.motor_pins[pin], step_sequence[car_object.motor_step_counter][pin] )
            if direction==True:
                car_object.motor_step_counter = (car_object.motor_step_counter - 1) % 8
            elif direction==False:
                car_object.motor_step_counter = (car_object.motor_step_counter + 1) % 8
            else: # defensive programming
                print( "CAR1_MOTOR: uh oh... direction should *always* be either True or False" )
                car_object.clean_up_motor_pins()
                exit( 1 )
            time.sleep( car_object.step_sleep )

def second_passed(oldepoch):
    return time.time() - oldepoch >= 1

def refresh_speed():
    curr_oldtime = time.time()
    while True:
        global car_object
        if second_passed(curr_oldtime):
            print("1 second passed")
            curr_oldtime = time.time()
        time.sleep(0.25)
        try:
            car_object.adjust_speed()
            print(car_object.step_sleep)
        except Exception as e:
            print(e, "Error occurred while adjusting speed.")

# where the entire program starts
if __name__ == "__main__":
    try:
        # Create a shared object for the car 1 object
        print("CAR1_MAIN: Creating Car 1...")

        # Create threads for each function
        receiver_thread = threading.Thread(target=receiver)
        motor_controller_thread = threading.Thread(target=motor_controller)
        refresh_speed_thread = threading.Thread(target=refresh_speed)

        # Start all threads
        receiver_thread.setDaemon(True)
        motor_controller_thread.setDaemon(True)
        refresh_speed_thread.setDaemon(True)

        receiver_thread.start()
        motor_controller_thread.start()
        refresh_speed_thread.start()

        receiver_thread.join()
        motor_controller_thread.join()
        refresh_speed_thread.join()


    except KeyboardInterrupt:
        print("CAR1_MAIN: Program stopped by user.")
        print("CAR1_MAIN: closing zigbee receiver AND transmitter, and cleaning up motor pins")
        car_object.close_zigbee_receiver()
        car_object.close_zigbee_transmitter()
        car_object.clean_up_motor_pins()