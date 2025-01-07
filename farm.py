from buildings import Building

class Farm(Building):
    def __init__(self):
        super().__init__(
            name="F",
            cost={"w": 60},
            build_time=10,
            health=100,
            max_health=100,
            longueur=2,
            dropPoint=True
        )
