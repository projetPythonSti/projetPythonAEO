from buildings import Building

class Keep(Building) :
  def __init__(self) :
    super().__init__(
      name="Keep",
      cost={"wood": 35, "gold": 125},
      time_building=80,
      health=800,
      longueur=1,
    )
