from buildings import Building

class Farm(Building) :
  def __init__(self) :
    super().__init__(
      name="F",
      cost={"Wood": 60},
      build_time=10,
      hp=100
      longueur=2,
      dropPoint=True
    )
