from unity.Unity import Unity

class Archer(Unity):
    
    def __init__(self, team):
        community = team.get_community().get('a')
        uid = len(community) if community else 0 # 0 if it doesn't exist yet
        super().__init__(uid, "A", { "wood" : 25, "gold" : 45}, 35, 30, 4, 1, 4, team = team)
    
