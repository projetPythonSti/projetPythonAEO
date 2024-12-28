from unity.Unity import Unity

class Horseman(Unity):
    
    def __init__(self, team):
        community = team.get_community().get('h')
        uid = len(community) if community else 0 # 0 if it doesn't exist yet
        super().__init__(uid, "h", { "f" : 80, "g" : 20}, 30, 45, 4, 1.2, 1, team=team)