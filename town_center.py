from building import Building

class TownCenter(Building):
    def __init__(self):
        super().__init__(
            name="Town Centre",
            cost={"wood": 350},
            time_building=150,
            health=1000,
            surface=16,  # 4x4
            population=5,
            dropPoint=True,
            spawn="Villager"
        )
