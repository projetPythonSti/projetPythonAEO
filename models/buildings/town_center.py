from models.buildings.buildings import Building

class TownCenter(Building):
    surface = (4, 4)  # 4x4
    def __init__(self, team):
        uid = f"eq{team.name}b{team.get_bldCount()}" # 0 if it doesn't exist yet
        super().__init__(
            uid,
            name="T",
            cost={"w": 350},
            time_building=150,
            health=1000,
            population=5,
            dropPoint=True,
            spawn="Villager",
            team=team
        )
