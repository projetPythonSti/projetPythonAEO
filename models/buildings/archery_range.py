from buildings import Building

class ArcheryRange(Building) :
  def __init__(self) :
    super().__init__(
      name="AR",
      cost={"wood": 175},
      time_building=50,
      health=500,
      length=3,  # 3x3
      spawn="Archer"
    )
