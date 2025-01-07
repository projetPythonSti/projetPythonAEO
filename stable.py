from buildings import Building

class Stable(Building):
    def __init__(self):
        super().__init(
            name="S",
            cost={"w": 175},
            time_building=50,
            health=500,
            max_health=500,
            longueur=3,
            spawn="h"
        )
