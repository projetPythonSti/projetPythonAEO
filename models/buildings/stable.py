from models.buildings.buildings import Building

class Stable(Building) :
  def __init__(self, team) :
    community = team.get_community().get('S')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name="S",
      cost={"w": 175},
      time_building=50,
      health=500,
      surface=(3,3),  # 3x3
      spawn="Horseman",
      team=team
    )
