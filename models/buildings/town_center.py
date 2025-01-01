from models.buildings.buildings import Building

class TownCenter(Building):
    def __init__(self, team):
        community = team.get_community().get('T')
        uid = len(community) if community else 0 # 0 if it doesn't exist yet
        super().__init__(
            uid,
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
