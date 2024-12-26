from buildings import Building

class Stable(Building) :
  def __init__(self) :
    super().__init(
      name="S",
      cost={"wood": 175},
      time_building=50,
      health=500,
      longueur=3,
      spawn="Horseman"
    )
