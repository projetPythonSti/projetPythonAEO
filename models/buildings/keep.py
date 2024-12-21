from buildings.buildings import Building

class Keep(Building) :
  def __init__(self) :
    super().__init__(
      name="K",
      cost={"wood": 35, "gold": 125},
      time_building=80,
      health=800,
      surface=1,  # 1x1
    )
