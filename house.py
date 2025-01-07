from building import Building

class House(Building):
    def __init__(self):
        super().__init__(
            name="H",
            cost={"w": 25},
            time_building=25,
            health=200,
            max_health=200,
            longueur=2,
            population=5
        )
