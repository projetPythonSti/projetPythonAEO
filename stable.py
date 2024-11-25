from buildings import Building

class Stable(Building) :
  def __init__(self) :
    super().__init(
      name="Stable",
      cost={"wood": 175},
      time_building=50,
      health=500,
      surface=3,
      spawn="Horseman"
    )
