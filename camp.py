from buildings import Building

class Camp(Building) :
   def __init__(self):
        super().__init__(
           name="C",
           cost={"wood": 100},
           time_building=25,
           health=200,
           longueur=2,
           dropPoint=True
       )
          
