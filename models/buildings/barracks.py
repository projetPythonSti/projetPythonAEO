from buildings import Building

class Barracks(Building) :
  def __init__(self) :
    super().__init__(
      name="B",
      cost={"wood": 175},
      time_building=50,
      health=500,
      length=3,  # 3x3
      spawn="Swordsman"
    )
