from buildings.buildings import Building

class Camp(Building) :
   def __init__(self, team) :
        super().__init__(
           name="C",
           cost={"w": 100},
           time_building=25,
           health=200,
           surface=(2,2),  # 2x2
           dropPoint=True,
           team=team
       )
          
