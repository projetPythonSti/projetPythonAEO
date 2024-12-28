from unity.Unity import Unity
# from model import Model

class Swordsman(Unity):
    def __init__(self, team):
        community = team.get_community().get('s')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid, "s", { "f" : 50, "g" : 20}, 20, 40, 4, 0.9, 1, team=team)