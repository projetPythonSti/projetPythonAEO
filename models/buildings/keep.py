from buildings.buildings import Building

class Keep(Building) :
  def __init__(self, team) :
    super().__init__(
      name="K",
      cost={"w": 35, "g": 125},
      time_building=80,
      health=800,
      surface=(1,1),  # 1x1
      team=team
    )
    self.damage = 5
    self.visibility = 8
