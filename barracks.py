from buildings import Building

class Barracks(Building):
    def __init__(self):
        super().__init__(
            name="B",
            cost={"w": 175},
            time_building=50,
            health=500,
            max_health=500,
            longueur=3,
            spawn="s"
        )
