from buildings import Building

class Farm(Building) :
  def __init__(self) :
    super().__init__(
      name="F",
      cost={"wood": 100},
      time_building=25,
      health=200,
      length=2,  # 2x2
      dropPoint=True
    )
