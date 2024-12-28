from buildings.buildings import Building

class House(Building):
    def __init__(self, team):
        super().__init__(
            name="H",
            cost={"w": 25},
            time_building=25,
            health=200,
            surface=(2,2),  # 2x2
            population=5,
            team=team
        )
