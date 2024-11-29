
from unity.Unity import Unity

class Swordsman(Unity):
    def __init__(self):
        super().__init__(id, "SM", { "food" : 50, "gold" : 20}, 20, 40, 4, 0.2, 1)