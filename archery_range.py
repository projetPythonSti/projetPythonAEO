from buildings import Building

class Archery_range(Building) :
  def __init__(self) :
    super().__ini__(
      name="Archery Range",
      cost={"wood": 175},
      time_building=50,
      health=500,
      surface=9,  # 3x3
      spawn="Archer"
    )
