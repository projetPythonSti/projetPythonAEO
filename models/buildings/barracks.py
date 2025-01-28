from models.buildings.buildings import Building

class Barracks(Building) :
  surface = (3, 3)  # 3x3
  def __init__(self, team) :
    uid = f"eq{team.name}b{team.get_bldCount()}"
    super().__init__(
      uid,
      name="B",
      cost={"w": 175},
      time_building=50,
      health=500,
      spawn="Swordsman",
      team=team
    )
