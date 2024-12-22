from models.buildings.buildings import Building

class ArcheryRange(Building) :
  def __init__(self) :
    super().__init__(
      name="AR",
      cost={"wood": 175},
      time_building=50,
      health=500,
      surface=9,  # 3x3
      spawn="Archer"
    )
