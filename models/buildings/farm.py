from models.buildings.buildings import Building
from models.ressources.ressources import Food

class Farm(Building):
  surface = (2, 2)  # 2x2
  def __init__(self, team):
    community = team.get_community().get('F')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name = "F",
      cost = {"w": 60},
      time_building = 10,
      health = 100,
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
