from buildings import Building

class House(Building):
    def __init__(self):
        super().__init__(
            name="H",
            cost={"wood": 25},
            time_building=25,
            health=200,
            length=2,  # 2x2
            population=5
        )
