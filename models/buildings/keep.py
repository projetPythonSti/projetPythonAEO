from models.buildings.buildings import Building

class Keep(Building) :
  surface = (1, 1),  # 1x1
  def __init__(self, team) :
    community = team.get_community().get('K')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name="K",
      cost={"w": 35, "g": 125},
      time_building=80,
      health=800,
      team=team
    )
    self.damage = 5
    self.visibility = 8
