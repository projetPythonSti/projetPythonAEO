from unity.Unity import Unity

class Horseman(Unity):
    
    def __init__(self, id, team):
        super().__init__(id, "HM", { "food" : 30, "gold" : 20}, 20, 45, 4, 1.2, 1, team=team)