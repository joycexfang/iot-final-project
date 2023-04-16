class Car:
  def __init__(self, rank, max_speed):
    self.rank = rank
    self.max_speed = max_speed
    self.curr_speed = 0

  def __str__(self):
    return "CAR self.rank: {} \t self.max_speed: {} \t self.curr_speed: {}".format(self.rank, self.max_speed, self.curr_speed)
  
  def change_speed(self):
    # todo: update code
    self.curr_speed = 5
    
    print("changed self.curr_speed to:", self.curr_speed)