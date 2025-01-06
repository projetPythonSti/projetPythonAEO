from models.buildings.buildings import Building

class Barracks(Building) :
  
  def __init__(self, team) :
    community = team.get_community().get('B')
    uid = len(community) if community else 0 # 0 if it doesn't exist yet
    super().__init__(
      uid,
      name="B",
      cost={"w": 175},
      time_building=50,
      health=500,
      surface=(3,3),  # 3x3
      spawn="Swordsman",
      team=team
    )
