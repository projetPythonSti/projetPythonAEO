from buildings import Building

class Barracks(Building) :
  def __init__(self) :
    super().__init__(
      name="Barracks",
      cost={"wood": 175},
      time_building=50,
      health=500,
      surface=9,  # 3x3
      spawn="Swordsman"
    )
