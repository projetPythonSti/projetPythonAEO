from buildings.buildings import Building
from ressources.ressources import Food

class Farm(Building):
  def __init__(self, team):
    super().__init__(
      name = "F",
      cost = {"w": 60},
      time_building = 10,
      health = 100,
      surface = (2,2),  # 2x2
      dropPoint = True,
      team = team
    )
    self.team = team
    self.contains = []
    self.max_capacity = 300
    
  def add_food(self, food):
    if len(self.contains) < self.max_capacity:
      self.contains.append(food)
      return True
    return False
