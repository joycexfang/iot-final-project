from class_car import Car

# This file is for the car 2 receiver main program
def main():
     # initialize the car 2 object
    car2 = Car(2, 30)

    try:
        # program for the car 2 receiver using Zigbee device
        while True:
            xbee_message = car2.receive_message()
            if xbee_message:
                data = xbee_message.data
                sender = xbee_message.remote_device
                timestamp = xbee_message.timestamp
                msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender, data=data.decode('UTF8'))
                print(msg)
    
    except KeyboardInterrupt:
        print('Keyboard was interrupted!')
    
    print("Closing car1 zigbee receiver")
    car2.close_zigbee()

if __name__ == "__main__":
    main()
