class TrafficLight:
    def __init__(self, initial_state):
        self.state = initial_state

    def __str__(self):
        return "TRAFFIC LIGHT self.state: {}".format(self.state)
  
    def change_state(self):
        # if the state of the light is red, change to green
        if self.state == "red":
            self.state = "green"
        # if the state of the light is green, change to yellow
        elif self.state == "green":
            self.state = "yellow"
        # otherwise (if the state of the light is yellow), change to red
        else:
            self.state = "red"

        print("changed self.state to:", self.state)