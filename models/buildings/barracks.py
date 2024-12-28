from buildings.buildings import Building

class Barracks(Building) :
  def __init__(self, team) :
    super().__init__(
      name="B",
      cost={"w": 175},
      time_building=50,
      health=500,
      surface=(3,3),  # 3x3
      spawn="Swordsman",
      team=team
    )
