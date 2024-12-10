from unity.Unity import Unity

class Horseman(Unity):
    
    def __init__(self, team):
        community = team.get_community().get('hm')
        uid = len(community) if community else 0 # 0 if it doesn't exist yet
        super().__init__(uid, "HM", { "food" : 30, "gold" : 20}, 20, 45, 4, 1.2, 1, team=team)