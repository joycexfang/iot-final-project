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

# main process for car 1 receiver
def receiver(car_object):
    # program for the car 1 receiver using Zigbee device
    while True:
        # Receive data
        print("CAR1_RECEIVER: Receiving data...")

        try:
            xbee_message = car_object.receive_message()
            if xbee_message:
                data = xbee_message.data

                # setting msg data so that transmit can occur
                car_object.set_msg_data(data)
                sender = xbee_message.remote_device
                timestamp = xbee_message.timestamp
                msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender, data=data.decode('UTF8'))
                print(msg)

                print("CAR1_RECEIVER: TODO: now that i've received data, need to change speed, have the motor controller change that speed, and transmit to next car")
        except Exception as e:
            print(e, "Error occurred while receiving message.")
            

# main process for car 1 transmitter
def transmitter(car_object):
    while True:
        # Send data to another device
        print("CAR1_TRANSMITTER: Transmitting data...")

        # check when car 1 needs to transmit data
        if car_object.get_need_transmit():
            message = car_object.get_msg_data
            print("CAR1_TRANSMITTER: Transmitting message:", message)
            car_object.transmit_message(message)
            try: 
                print("CAR1_TRANSMITTER: Will try transmitting message from car 1 to car 2:", message)
                car_object.transmit_message(message)
            except Exception as e:
                print(e, "CAR1_TRANSMITTER: No car is listening.")
            print()

# main process for car 1 motor controller
def motor_controller(car_object):
    while True:
        # Control a motor or other actuator
        print("CAR1_MOTOR: Controlling motor...")

        # the meat
        i = 0
        for i in range(step_count):
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
       
        car_object.clean_up_motor_pins()
        exit( 0 )

def second_passed(oldepoch):
    return time.time() - oldepoch >= 1

def refresh_speed(car_proxy):
    curr_oldtime = time.time()
    car_object: Car = car_proxy.value
    while True:
        if second_passed(curr_oldtime):
            print("1 second passed")
            curr_oldtime = time.time()
        time.sleep(0.25)
        try:
            #car_object.adjust_speed()
            car_object.step_sleep += 0.001
        except Exception as e:
            print(e, "Error occurred while adjusting speed.")
        print("0.25 seconds passed")

# where the entire program starts
if __name__ == "__main__":
    try:
        # Create a shared proxy object for the car 1 object
        print("CAR1_MAIN: Creating Car 1...")
        car1 = Car(1, 30)

        # Create threads for each function
        receiver_thread = threading.Thread(target=receiver, args=(car1,))
        transmitter_thread = threading.Thread(target=transmitter, args=(car1,))
        motor_controller_thread = threading.Thread(target=motor_controller, args=(car1,))
        refresh_speed_thread = threading.Thread(target=refresh_speed, args=(car1,))

        # Start all threads
        receiver_thread.setDaemon(True)
        transmitter_thread.setDaemon(True)
        motor_controller_thread.setDaemon(True)
        refresh_speed_thread.setDaemon(True)

        receiver_thread.start()
        transmitter_thread.start()
        motor_controller_thread.start()
        refresh_speed_thread.start()

        receiver_thread.join()
        transmitter_thread.join()
        motor_controller_thread.join()
        refresh_speed_thread.join()


    except KeyboardInterrupt:
        print("CAR1_MAIN: Program stopped by user.")
        print("CAR1_MAIN: closing zigbee receiver AND transmitter, and cleaning up motor pins")
        car1.value.close_zigbee_receiver()
        car1.value.close_zigbee_transmitter()
        car1.value.clean_up_motor_pins()
