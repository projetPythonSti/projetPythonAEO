from models.buildings.buildings import Building

class Camp(Building) :
   surface = (2, 2),  # 2x2
   def __init__(self, team) :
      community = team.get_community().get('C'),
      uid = len(community) if community else 0 # 0 if it doesn't exist yet
      super().__init__(
         uid,
         name="C",
         cost={"w": 100},
         time_building=25,
         health=200,
         dropPoint=True,
         team=team
      )
          
