from models.buildings.buildings import Building

class ArcheryRange(Building) :
  surface = (3, 3)  # 3x3
  def __init__(self, team) :
    community = team.get_community().get('A')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name="A",
      cost={"w": 175},
      time_building=50,
      health=500,
      spawn="Archer",
      team=team
    )
