from models.buildings.buildings import Building

class House(Building):
    surface = (2, 2),  # 2x2
    def __init__(self, team):
        community = team.get_community().get('H')
        uid = len(community) if community else 0 # 0 if it doesn't exist yet
        super().__init__(
            uid,
            name="H",
            cost={"w": 25},
            time_building=25,
            health=200,
            population=5,
            team=team
        )
