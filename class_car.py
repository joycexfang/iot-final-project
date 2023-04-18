import math # import math library
import time # import the time module
from class_traffic_light import TrafficLight
import datetime

tracking = time.time()

class Car:
    def __init__(self, rank, max_speed, traffic_light):
        self.rank = rank
        self.max_speed = max_speed
        self.curr_speed = 0
        self.traffic_light = traffic_light

    def __str__(self):
        return "CAR self.rank: {} \t self.max_speed: {} \t self.curr_speed: {}".format(self.rank, self.max_speed, self.curr_speed)

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

