from unity.Unity import Unity
# from model import Model

class Swordsman(Unity):
    def __init__(self, team):
        community = team.get_community().get('sm')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid, "SM", { "food" : 50, "gold" : 20}, 20, 40, 4, 0.2, 1, team=team)