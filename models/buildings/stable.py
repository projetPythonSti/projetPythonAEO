from buildings import Building

class Stable(Building) :
  def __init__(self) :
    super().__init(
      name="S",
      cost={"wood": 175},
      time_building=50,
      health=500,
      length=3,  # 3x3
      spawn="Horseman"
    )
