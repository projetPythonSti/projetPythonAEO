from buildings import Building

class Keep(Building):
    def __init__(self):
        super().__init__(
            name="K",
            cost={"w": 35, "g": 125},
            time_building=80,
            health=800,
            max_health=800,
            longueur=1,
        )
