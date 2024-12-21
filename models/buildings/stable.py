from buildings.buildings import Building

class Stable(Building) :
  def __init__(self) :
    super().__init(
      name="S",
      cost={"wood": 175},
      time_building=50,
      health=500,
      surface=9,  # 3x3
      spawn="Horseman"
    )
