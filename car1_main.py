import multiprocessing
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
def receiver(car_proxy):
    car_object: Car = car_proxy.value
    # program for the car 1 receiver using Zigbee device
    while True:
        # Receive data
        print("Receiving data...")
        xbee_message = car_object.receive_message()
        if xbee_message:
            data = xbee_message.data
            sender = xbee_message.remote_device
            timestamp = xbee_message.timestamp
            msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender, data=data.decode('UTF8'))
            print(msg)

# main process for car 1 transmitter
def transmitter(car_proxy):
    car_object: Car = car_proxy.value
    while True:
        # Send data to another device
        print("Transmitting data...")
      
# main process for car 1 motor controller
def motor_controller(car_proxy):
    car_object: Car = car_proxy.value
    while True:
        # Control a motor or other actuator
        print("Controlling motor...")

        # the meat
        try:
            i = 0
            for i in range(step_count):
                for pin in range(0, len(car_object.motor_pins)):
                    GPIO.output( car_object.motor_pins[pin], step_sequence[car_object.motor_step_counter][pin] )
                if direction==True:
                    car_object.motor_step_counter = (car_object.motor_step_counter - 1) % 8
                elif direction==False:
                    car_object.motor_step_counter = (car_object.motor_step_counter + 1) % 8
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    car_object.cleanup()
                    exit( 1 )
                time.sleep( car_object.step_sleep )
        except KeyboardInterrupt:
            car_object.cleanup()
            exit( 1 )

        car_object.cleanup()
        exit( 0 )

# where the entire program starts
if __name__ == "__main__":
    # Create a shared proxy object for the car 1 object
    manager = multiprocessing.Manager()
    print("Creating Car 1...")
    car1_proxy = manager.Value("Car1", Car(1, 30))

    # Create three processes for each function
    receiver_process = multiprocessing.Process(target=receiver, args=(car1_proxy,))
    transmitter_process = multiprocessing.Process(target=transmitter, args=(car1_proxy,))
    motor_controller_process = multiprocessing.Process(target=motor_controller, args=(car1_proxy,))

    # Start all three processes
    receiver_process.start()
    transmitter_process.start()
    motor_controller_process.start()

    # Wait for all three processes to finish
    receiver_process.join()
    transmitter_process.join()
    motor_controller_process.join()
