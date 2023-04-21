from class_car import Car

# This file is for the car 1 receiver main program
def main():
     # initialize the car 1 object
    car1 = Car(1, 30)

    try:
        # program for the car 1 receiver using Zigbee device
        while True:
            xbee_message = car1.receive_message()
            if xbee_message:
                data = xbee_message.data
                sender = xbee_message.remote_device
                timestamp = xbee_message.timestamp
                msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender, data=data.decode('UTF8'))
                print(msg)
    
    except KeyboardInterrupt:
        print('Keyboard was interrupted!')
    
    print("Closing car1 zigbee receiver")
    car1.close_zigbee()

if __name__ == "__main__":
    main()
