from buildings import Building

class TownCenter(Building):
    def __init__(self):
        super().__init__(
            name="T",
            cost={"wood": 350},
            time_building=150,
            health=1000,
            length=4,  # 4x4
            population=5,
            dropPoint=True,
            spawn="Villager"
        )
