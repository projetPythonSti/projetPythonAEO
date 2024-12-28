from buildings.buildings import Building

class TownCenter(Building):
    def __init__(self, team):
        super().__init__(
            name="T",
            cost={"w": 350},
            time_building=150,
            health=1000,
            surface=(4,4),  # 4x4
            population=5,
            dropPoint=True,
            spawn="Villager",
            team=team
        )
