# Vehicle and Traffic Light Network Interfacing Project

IOT 4660 - Internetworking of Things

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

1. Traffic Light - 1 x Zigbee Transmitter (PAN ID = 727)

   1 x Raspberry Pi 3 B+

2. Car 1 - 1 x Zigbee Receiver (PAN ID = 727),

   1 x Zigbee Transmitter (PAN ID = 202)

   1 x Raspberry Pi 3 B+

   1 x Driver - ULN2003

   1 x Step Motor - 28BYJ-48

3. Car 2 - 1 x Zigbee Receiver (PAN ID = 202)

   1 x Raspberry Pi 3 B+

   1 x Driver - ULN2003

   1 x Step Motor - 28BYJ-48

## install dependencies for python3

`sudo apt-get install python3-dev python3-pip -y`

`pip3 install digi-xbee`

## how to run traffic light transmitter

`python3 traffic_light_main.py`

## how to run car 1

`python3 car1_main.py`

## how to run car 2

`python3 car2_main.py`

## IP Addresses

Traffic Light RPi: `pi@191.168.1.157`

Car 1 RPi: `shibata@191.168.1.19`

Car 2 RPi: `pi@191.168.1.127`

# Instructions to SCP files from local machine to RPi

1. on your local machine, open terminal

2. cd into the directory where your python files are

3. run the following command on local machine:

`scp <name_of_this_project_directory> -r username@<ip address>:/home/{username}`

# Joyce's Notes

CAR 1:

scp iot-final-project -r shibata@191.168.1.19:/home/shibata

TRAFFIC LIGHT:

scp iot-final-project -r pi@191.168.1.157:/home/pi

CAR 2:

scp iot-final-project -r pi@191.168.1.127:/home/pi
